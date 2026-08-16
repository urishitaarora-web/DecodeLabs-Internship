import io
import os
from typing import Any

import pandas as pd

from fastapi import APIRouter, Depends, HTTPException
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
    SUPABASE_SERVICE_ROLE_KEY,
)

DATASET_BUCKET = "datasets"

router = APIRouter(
    prefix="/analysis",
    tags=["Analysis"],
)


# ============================================================
# HELPERS
# ============================================================

def _get_user_id(user: Any) -> str:
    if isinstance(user, dict):
        user_id = user.get("sub")
    else:
        user_id = user

    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Authenticated user ID not found.",
        )

    return user_id


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
                detail="Dataset not found.",
            )

        return result.data

    except HTTPException:
        raise

    except Exception as exc:
        print(
            "ANALYSIS DATASET LOOKUP ERROR:",
            repr(exc),
        )

        raise HTTPException(
            status_code=400,
            detail="Unable to load dataset.",
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
        return (
            supabase
            .storage
            .from_(DATASET_BUCKET)
            .download(storage_path)
        )

    except Exception as exc:
        print(
            "ANALYSIS DATASET DOWNLOAD ERROR:",
            repr(exc),
        )

        raise HTTPException(
            status_code=400,
            detail="Unable to download dataset.",
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

    except Exception as exc:
        print(
            "ANALYSIS FILE READ ERROR:",
            repr(exc),
        )

        raise HTTPException(
            status_code=400,
            detail=f"Unable to read dataset: {str(exc)}",
        )

    raise HTTPException(
        status_code=400,
        detail=(
            "Unsupported file type. "
            "Use CSV, XLSX, or JSON."
        ),
    )


def _safe_number(value):
    if pd.isna(value):
        return None

    if hasattr(value, "item"):
        value = value.item()

    if isinstance(value, float):
        if pd.isna(value):
            return None

        return round(value, 6)

    return value


def _safe_value(value):
    if pd.isna(value):
        return None

    if hasattr(value, "item"):
        value = value.item()

    return value


# ============================================================
# MAIN EDA ENDPOINT
# ============================================================

@router.get("/dataset/{dataset_id}")
async def analyze_saved_dataset(
    dataset_id: str,
    user=Depends(verify_clerk_token),
):
    """
    Run exploratory data analysis on a dataset already
    saved in Supabase Storage.

    This endpoint does NOT modify the dataset.
    """

    user_id = _get_user_id(user)

    # --------------------------------------------------------
    # 1. LOAD DATASET METADATA
    # --------------------------------------------------------

    dataset = _get_dataset_for_user(
        dataset_id,
        user_id,
    )

    # --------------------------------------------------------
    # 2. DOWNLOAD DATASET
    # --------------------------------------------------------

    raw = _download_dataset(dataset)

    # --------------------------------------------------------
    # 3. LOAD DATAFRAME
    # --------------------------------------------------------

    df = _load_dataframe(
        dataset["filename"],
        raw,
    )

    # --------------------------------------------------------
    # 4. BASIC DATASET METRICS
    # --------------------------------------------------------

    total_rows = len(df)
    total_columns = len(df.columns)

    total_cells = total_rows * total_columns

    missing_values = int(
        df.isna().sum().sum()
    )

    missing_percentage = (
        round(
            (missing_values / total_cells) * 100,
            2,
        )
        if total_cells
        else 0
    )

    duplicate_rows = int(
        df.duplicated().sum()
    )

    duplicate_percentage = (
        round(
            (duplicate_rows / total_rows) * 100,
            2,
        )
        if total_rows
        else 0
    )

    # --------------------------------------------------------
    # 5. COLUMN TYPES
    # --------------------------------------------------------

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()

    categorical_columns = df.select_dtypes(
        include=["object", "category", "bool"]
    ).columns.tolist()

    datetime_columns = df.select_dtypes(
        include=["datetime", "datetimetz"]
    ).columns.tolist()

    # --------------------------------------------------------
    # 6. COLUMN ANALYSIS
    # --------------------------------------------------------

    columns = []

    for column in df.columns:

        series = df[column]

        missing = int(
            series.isna().sum()
        )

        unique = int(
            series.nunique(
                dropna=True
            )
        )

        column_info = {
            "name": str(column),
            "dtype": str(series.dtype),
            "missing": missing,
            "missing_percentage": (
                round(
                    (missing / total_rows) * 100,
                    2,
                )
                if total_rows
                else 0
            ),
            "unique": unique,
            "unique_percentage": (
                round(
                    (unique / total_rows) * 100,
                    2,
                )
                if total_rows
                else 0
            ),
            "is_numeric": column in numeric_columns,
            "is_categorical": column in categorical_columns,
            "is_datetime": column in datetime_columns,
             "statistics": (
                {
                    "sum": _safe_number(series.sum()),
                    "mean": _safe_number(series.mean()),
                    "median": _safe_number(series.median()),
                    "variance": _safe_number(series.var()),
                    "std": _safe_number(series.std()),
                    "min": _safe_number(series.min()),
                    "max": _safe_number(series.max()),
                }
                if column in numeric_columns
                else None
            ),
        }
        columns.append(column_info)
        # Numeric statistics
        if column in numeric_columns:

            numeric_series = pd.to_numeric(
                series,
                errors="coerce",
            )

            column_info["statistics"] = {
                "sum": _safe_number(
                    numeric_series.sum()
                ),
                "mean": _safe_number(
                    numeric_series.mean()
                ),
                "median": _safe_number(
                    numeric_series.median()
                ),
                "variance": _safe_number(
                     numeric_series.var()
                ),
                "std": _safe_number(
                    numeric_series.std()
                ),
                "min": _safe_number(
                    numeric_series.min()
                ),
                "max": _safe_number(
                    numeric_series.max()
                ),
            }

        # Categorical information
        elif column in categorical_columns:

            value_counts = (
                series
                .astype(str)
                .value_counts()
                .head(10)
            )

            column_info["top_values"] = [
                {
                    "value": str(index),
                    "count": int(count),
                }
                for index, count
                in value_counts.items()
            ]

        columns.append(
            column_info
        )

    # --------------------------------------------------------
    # 7. MISSING VALUE ANALYSIS
    # --------------------------------------------------------

    missing_analysis = []

    for column in df.columns:

        missing = int(
            df[column].isna().sum()
        )

        if missing == 0:
            continue

        percentage = (
            round(
                (missing / total_rows) * 100,
                2,
            )
            if total_rows
            else 0
        )

        severity = "low"

        if percentage >= 50:
            severity = "high"
        elif percentage >= 10:
            severity = "medium"

        missing_analysis.append({
            "column": str(column),
            "missing": missing,
            "percentage": percentage,
            "severity": severity,
        })

    missing_analysis.sort(
        key=lambda item: item["percentage"],
        reverse=True,
    )

    # --------------------------------------------------------
    # 8. CORRELATION MATRIX
    # --------------------------------------------------------

    correlations = {}

    if len(numeric_columns) >= 2:

        correlation_df = (
            df[numeric_columns]
            .corr()
            .round(4)
        )

        correlations = {
            str(column): {
                str(other_column): _safe_number(
                    correlation_df.loc[
                        column,
                        other_column,
                    ]
                )
                for other_column in numeric_columns
            }
            for column in numeric_columns
        }

    # --------------------------------------------------------
    # 9. SIMPLE AUTOMATED INSIGHTS
    # --------------------------------------------------------

    insights = []

    if missing_values == 0:
        insights.append({
            "type": "success",
            "title": "No missing values",
            "message": (
                "The dataset contains no missing cells."
            ),
        })
    else:
        highest_missing = (
            missing_analysis[0]
            if missing_analysis
            else None
        )

        if highest_missing:
            insights.append({
                "type": "warning",
                "title": "Missing data detected",
                "message": (
                    f"{highest_missing['column']} has "
                    f"{highest_missing['percentage']}% "
                    "missing values."
                ),
            })

    if duplicate_rows == 0:
        insights.append({
            "type": "success",
            "title": "No duplicate rows",
            "message": (
                "No exact duplicate records were detected."
            ),
        })
    else:
        insights.append({
            "type": "warning",
            "title": "Duplicate rows detected",
            "message": (
                f"{duplicate_rows:,} duplicate rows "
                "were detected."
            ),
        })

    constant_columns = [
        str(column)
        for column in df.columns
        if df[column].nunique(
            dropna=False
        ) <= 1
    ]

    if constant_columns:
        insights.append({
            "type": "warning",
            "title": "Constant columns detected",
            "message": (
                f"{len(constant_columns)} column(s) "
                "contain only one unique value."
            ),
            "columns": constant_columns,
        })

    if len(numeric_columns) > 0:
        insights.append({
            "type": "info",
            "title": "Numeric features detected",
            "message": (
                f"{len(numeric_columns)} numeric "
                "column(s) are available for statistical analysis."
            ),
        })

    if len(categorical_columns) > 0:
        insights.append({
            "type": "info",
            "title": "Categorical features detected",
            "message": (
                f"{len(categorical_columns)} categorical "
                "column(s) were identified."
            ),
        })

    # --------------------------------------------------------
    # 10. PREVIEW
    # --------------------------------------------------------

    preview_df = df.head(10)

    preview = []

    for _, row in preview_df.iterrows():

        preview.append({
            str(column): _safe_value(
                row[column]
            )
            for column in df.columns
        })

    # --------------------------------------------------------
    # 11. RESPONSE
    # --------------------------------------------------------

    return {
        "status": "success",

        "dataset": {
            "id": dataset_id,
            "filename": dataset["filename"],
            "rows": total_rows,
            "columns": total_columns,
            "missing_values": missing_values,
            "missing_percentage": missing_percentage,
            "duplicates": duplicate_rows,
            "duplicate_percentage": duplicate_percentage,
            "data_quality": dataset.get(
                "data_quality"
            ),
        },

        "composition": {
            "numeric": len(
                numeric_columns
            ),
            "categorical": len(
                categorical_columns
            ),
            "datetime": len(
                datetime_columns
            ),
        },

        "column_types": {
            "numeric": [
                str(column)
                for column in numeric_columns
            ],
            "categorical": [
                str(column)
                for column in categorical_columns
            ],
            "datetime": [
                str(column)
                for column in datetime_columns
            ],
        },

        "columns": columns,

        "missing_analysis": missing_analysis,

        "correlations": correlations,

        "insights": insights,

        "preview": preview,
    }