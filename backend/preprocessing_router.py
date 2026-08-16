import io
import json
import os

import pandas as pd

from fastapi import APIRouter, Form, Depends, HTTPException
from pydantic import BaseModel, Field

from preprocessing import run_basic_pipeline
from clerk_auth import verify_clerk_token

from supabase import create_client, Client
from dotenv import load_dotenv


load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
    raise RuntimeError("Supabase credentials are missing.")

supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_SERVICE_ROLE_KEY
)

DATASET_BUCKET = "datasets"

router = APIRouter()


class PreprocessConfig(BaseModel):
    missing_values: dict = Field(
        default_factory=lambda: {
            "enabled": True,
            "strategy": "auto",
        }
    )

    duplicates: dict = Field(
        default_factory=lambda: {
            "enabled": True,
            "keep": "first",
        }
    )

    outliers: dict = Field(
        default_factory=lambda: {
            "enabled": True,
            "method": "iqr",
            "action": "flag",
        }
    )


def _load_dataframe(
    filename: str,
    raw: bytes,
) -> pd.DataFrame:

    filename = (filename or "").lower()

    try:

        if filename.endswith(".csv"):
            return pd.read_csv(
                io.BytesIO(raw)
            )

        if filename.endswith((".xlsx", ".xls")):
            return pd.read_excel(
                io.BytesIO(raw)
            )

        if filename.endswith(".json"):
            return pd.read_json(
                io.BytesIO(raw)
            )

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=f"Unable to read dataset: {str(e)}",
        )

    raise HTTPException(
        status_code=400,
        detail="Unsupported file type. Use CSV, XLSX, or JSON.",
    )


def _get_dataset_for_user(
    dataset_id: str,
    user_id: str,
):
    try:

        result = (
            supabase
            .table("datasets")
            .select("*")
            .eq("id", dataset_id)
            .eq("user_id", user_id)
            .single()
            .execute()
        )

        if not result.data:
            raise HTTPException(
                status_code=404,
                detail="Dataset not found."
            )

        return result.data

    except HTTPException:
        raise

    except Exception as e:

        print(
            "DATASET LOOKUP ERROR:",
            repr(e)
        )

        raise HTTPException(
            status_code=400,
            detail="Unable to load dataset."
        )


def _download_dataset(dataset):
    storage_path = dataset.get("storage_path")

    if not storage_path:
        raise HTTPException(
            status_code=400,
            detail=(
                "This dataset does not have a stored file. "
                "Please upload the dataset again."
            ),
        )

    try:

        raw = (
            supabase
            .storage
            .from_(DATASET_BUCKET)
            .download(storage_path)
        )

        return raw

    except Exception as e:

        print(
            "DATASET DOWNLOAD ERROR:",
            repr(e)
        )

        raise HTTPException(
            status_code=400,
            detail=f"Unable to download dataset: {str(e)}",
        )


@router.post("/preprocess-dataset")
async def preprocess_dataset(
    dataset_id: str = Form(...),
    config: str = Form(default="{}"),
    user=Depends(verify_clerk_token),
):
    """
    Run preprocessing using a dataset already saved
    in Supabase Storage.
    """

    user_id = user["sub"] if isinstance(user, dict) else user

    # --------------------------------------------------
    # STEP 1: Get dataset metadata
    # --------------------------------------------------

    dataset = _get_dataset_for_user(
        dataset_id,
        user_id,
    )

    # --------------------------------------------------
    # STEP 2: Download actual dataset file
    # --------------------------------------------------

    raw = _download_dataset(dataset)

    # --------------------------------------------------
    # STEP 3: Convert file into DataFrame
    # --------------------------------------------------

    df = _load_dataframe(
        dataset["filename"],
        raw,
    )

    # --------------------------------------------------
    # STEP 4: Parse preprocessing configuration
    # --------------------------------------------------

    try:

        parsed_config = json.loads(config)

        preprocess_config = PreprocessConfig(
            **parsed_config
        )

    except json.JSONDecodeError:

        raise HTTPException(
            status_code=400,
            detail="Invalid preprocessing configuration JSON.",
        )

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=f"Invalid preprocessing configuration: {str(e)}",
        )

    # --------------------------------------------------
    # STEP 5: Run preprocessing
    # --------------------------------------------------

    try:

        cleaned_df, report = run_basic_pipeline(
            df,
            preprocess_config.model_dump(),
        )

        preview = json.loads(
            cleaned_df
            .head(20)
            .to_json(
                orient="records",
                date_format="iso",
            )
        )

        return {
            "status": "success",

            "dataset_id": dataset_id,

            "filename": dataset["filename"],

            "report": report,

            "preview": preview,

            "columns": cleaned_df.columns.tolist(),

            "row_count": len(cleaned_df),
        }

    except Exception as e:

        print(
            "PREPROCESSING ERROR:",
            repr(e),
        )

        raise HTTPException(
            status_code=400,
            detail=f"Preprocessing failed: {str(e)}",
        )


@router.post("/preprocess-recommendations")
async def preprocess_recommendations(
    dataset_id: str = Form(...),
    user=Depends(verify_clerk_token),
):
    """
    Analyze a saved dataset and recommend preprocessing
    operations without modifying the dataset.
    """

    user_id = user["sub"] if isinstance(user, dict) else user

    # --------------------------------------------------
    # GET DATASET
    # --------------------------------------------------

    dataset = _get_dataset_for_user(
        dataset_id,
        user_id,
    )

    # --------------------------------------------------
    # DOWNLOAD FILE
    # --------------------------------------------------

    raw = _download_dataset(dataset)

    # --------------------------------------------------
    # LOAD DATAFRAME
    # --------------------------------------------------

    df = _load_dataframe(
        dataset["filename"],
        raw,
    )

    recommendations = []

    # --------------------------------------------------
    # Missing values
    # --------------------------------------------------

    missing_percentage = df.isna().mean()

    for column, percentage in missing_percentage[
        missing_percentage > 0
    ].items():

        if percentage > 0.5:

            recommendations.append({
                "type": "missing_values",
                "column": str(column),
                "severity": "high",
                "message": (
                    f"{column} is "
                    f"{percentage:.0%} missing — "
                    "consider dropping the column."
                ),
            })

        else:

            recommendations.append({
                "type": "missing_values",
                "column": str(column),
                "severity": "medium",
                "message": (
                    f"{column} has "
                    f"{percentage:.0%} missing values — "
                    "fill with median/mode."
                ),
            })

    # --------------------------------------------------
    # Duplicate rows
    # --------------------------------------------------

    duplicate_count = int(
        df.duplicated().sum()
    )

    if duplicate_count > 0:

        recommendations.append({
            "type": "duplicates",
            "column": None,
            "severity": "medium",
            "message": (
                f"{duplicate_count} duplicate rows "
                "found — recommend removal."
            ),
        })

    # --------------------------------------------------
    # Outliers
    # --------------------------------------------------

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns

    for column in numeric_columns:

        series = df[column]

        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)

        iqr = q3 - q1

        if pd.isna(iqr) or iqr == 0:
            continue

        lower = q1 - (1.5 * iqr)
        upper = q3 + (1.5 * iqr)

        outlier_count = int(
            (
                (series < lower)
                | (series > upper)
            ).sum()
        )

        if outlier_count > 0:

            recommendations.append({
                "type": "outliers",
                "column": str(column),
                "severity": "low",
                "message": (
                    f"{column} has "
                    f"{outlier_count} potential outliers "
                    "(IQR method)."
                ),
            })

    return {
        "status": "success",
        "dataset_id": dataset_id,
        "filename": dataset["filename"],
        "recommendations": recommendations,
    }