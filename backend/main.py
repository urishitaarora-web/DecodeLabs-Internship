from statistics import correlation

from fastapi import FastAPI, UploadFile, File, Form,HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

import pandas as pd
import io
import os
import json
import uuid
from dotenv import load_dotenv
from supabase import create_client, Client

from clerk_backend_api import Clerk
from clerk_backend_api import authenticate_request, AuthenticateRequestOptions
from preprocessing_router import router as preprocessing_router
from analysis_router import router as analysis_router
from eda_router import router as eda_router
load_dotenv()
CLERK_SECRET_KEY = os.getenv("CLERK_SECRET_KEY")

if not CLERK_SECRET_KEY:
    raise RuntimeError("Clerk server credentials are missing.")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
    raise RuntimeError("Supabase server credentials are missing.")

supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_SERVICE_ROLE_KEY
)
clerk = Clerk(
    bearer_auth=CLERK_SECRET_KEY
)
def require_user(request: Request) -> str:
    state = authenticate_request(
        request,
        AuthenticateRequestOptions(
            secret_key=CLERK_SECRET_KEY,
            authorized_parties=[
                "http://localhost:5173",
                 "http://127.0.0.1:5173",
                "https://cognify-frontend-bggv.onrender.com",
            ],
        ),
    )

    if not state.is_signed_in:
        raise HTTPException(
            status_code=401,
            detail="Authentication required."
        )

    return state.payload["sub"]
app = FastAPI(title="Cognify ML Backend")
app.include_router(analysis_router)
app.include_router(preprocessing_router)
app.include_router(eda_router)


# Allow React/Vite frontend to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://cognify-frontend-bggv.onrender.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "Cognify ML Backend is running",
        "status": "online"
    }


@app.post("/analyze-dataset")
async def analyze_dataset(file: UploadFile = File(...)):

    filename = file.filename.lower()

    allowed_extensions = [".csv", ".xlsx", ".json"]

    if not any(filename.endswith(ext) for ext in allowed_extensions):
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Use CSV, XLSX, or JSON."
        )

    contents = await file.read()

    try:

        # -----------------------------
        # READ DATASET
        # -----------------------------

        if filename.endswith(".csv"):

            df = pd.read_csv(
                io.BytesIO(contents)
            )

        elif filename.endswith(".xlsx"):

            df = pd.read_excel(
                io.BytesIO(contents)
            )

        elif filename.endswith(".json"):

            df = pd.read_json(
                io.BytesIO(contents)
            )

        # -----------------------------
        # BASIC INFORMATION
        # -----------------------------

        rows = len(df)
        columns = len(df.columns)

        # -----------------------------
        # MISSING VALUES
        # -----------------------------

        missing_values = int(
            df.isnull().sum().sum()
        )

        missing_percentage = round(
            (missing_values / df.size) * 100,
            2
        ) if df.size else 0

        # -----------------------------
        # DUPLICATES
        # -----------------------------

        duplicates = int(
            df.duplicated().sum()
        )

        # -----------------------------
        # COLUMN TYPES
        # -----------------------------

        numerical_columns = df.select_dtypes(
            include=["number"]
        ).columns.tolist()

        categorical_columns = df.select_dtypes(
            include=["object", "category", "bool"]
        ).columns.tolist()

        datetime_columns = df.select_dtypes(
            include=["datetime"]
        ).columns.tolist()

        # -----------------------------
        # DATA QUALITY SCORE
        # -----------------------------

        score = 100

        if missing_percentage > 0:
            score -= min(
                missing_percentage,
                30
            )

        if rows > 0:
            duplicate_percentage = (
                duplicates / rows
            ) * 100

            score -= min(
                duplicate_percentage,
                20
            )

        score = max(
            round(score, 2),
            0
        )

        # -----------------------------
        # COLUMN INFORMATION
        # -----------------------------

        column_details = []

        for column in df.columns:

            column_details.append({
                "name": str(column),
                "type": str(df[column].dtype),
                "missing": int(df[column].isnull().sum()),
                "unique": int(df[column].nunique())
            })

        # -----------------------------
        # RESPONSE
        # -----------------------------

        return {
            "success": True,
            "filename": file.filename,

            "dataset": {
                "rows": rows,
                "columns": columns,
                "missing_values": missing_values,
                "missing_percentage": missing_percentage,
                "duplicates": duplicates,
                "data_quality": score
            },

            "column_types": {
                "numerical": numerical_columns,
                "categorical": categorical_columns,
                "datetime": datetime_columns
            },

            "columns": column_details
        }

    except Exception as e:
       print("DATASET ANALYSIS ERROR:", repr(e))

       raise HTTPException(
         status_code=400,
         detail=f"Unable to analyze dataset: {str(e)}"
       )
from pydantic import BaseModel


class DatasetMetadata(BaseModel):
    rows: int
    columns: int
    missing_values: int
    missing_percentage: float
    duplicates: int
    data_quality: float
    column_types: dict
    columns_info: list
    status: str = "Analyzed"


@app.post("/save-dataset")
async def save_dataset(
    request: Request,
    file: UploadFile = File(...),
    metadata: str = Form(default="{}"),  
):
    user_id = require_user(request)

    filename = file.filename or "dataset"

    allowed_extensions = [".csv", ".xlsx", ".json"]

    if not any(
        filename.lower().endswith(ext)
        for ext in allowed_extensions
    ):
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Use CSV, XLSX, or JSON."
        )

    try:
        parsed_metadata = DatasetMetadata.model_validate_json(
            metadata
        )

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid dataset metadata: {str(e)}"
        )

    try:
        # ----------------------------------------
        # READ FILE
        # ----------------------------------------

        contents = await file.read()

        if not contents:
            raise HTTPException(
                status_code=400,
                detail="Uploaded dataset is empty."
            )

        # ----------------------------------------
        # CREATE STORAGE PATH
        # ----------------------------------------

        dataset_id = str(uuid.uuid4())

        safe_filename = filename.replace("/", "_")

        storage_path = (
            f"{user_id}/{dataset_id}/{safe_filename}"
        )

        # ----------------------------------------
        # UPLOAD TO SUPABASE STORAGE
        # ----------------------------------------

        supabase.storage \
            .from_("datasets") \
            .upload(
                storage_path,
                contents,
                {
                    "content-type":
                        file.content_type
                        or "application/octet-stream",
                    "upsert": "false",
                }
            )

        # ----------------------------------------
        # SAVE METADATA
        # ----------------------------------------

        result = (
            supabase
            .table("datasets")
            .insert({
                "id": dataset_id,
                "user_id": user_id,
                "filename": filename,
                "storage_path": storage_path,

                "file_size": len(contents),

                "rows": parsed_metadata.rows,
                "columns": parsed_metadata.columns,

                "missing_values":
                    parsed_metadata.missing_values,

                "missing_percentage":
                    parsed_metadata.missing_percentage,

                "duplicates":
                    parsed_metadata.duplicates,

                "data_quality":
                    parsed_metadata.data_quality,

                "column_types":
                    parsed_metadata.column_types,

                "columns_info":
                    parsed_metadata.columns_info,

                "status":
                    parsed_metadata.status,
            })
            .execute()
        )

        return {
            "success": True,
            "dataset": (
                result.data[0]
                if result.data
                else None
            ),
        }

    except Exception as e:

        print(
            "DATASET SAVE ERROR:",
            repr(e)
        )

        # ----------------------------------------
        # CLEANUP STORAGE IF DB INSERT FAILS
        # ----------------------------------------

        try:
            supabase.storage \
                .from_("datasets") \
                .remove([storage_path])
        except Exception:
            pass

        raise HTTPException(
            status_code=400,
            detail=f"Unable to save dataset: {str(e)}"
        )
@app.get("/datasets")
async def get_datasets(request: Request):
    user_id = require_user(request)

    try:
        result = (
            supabase
            .table("datasets")
            .select("*")
            .eq("user_id", user_id)
            .order("created_at", desc=True)
            .execute()
        )

        return {
            "success": True,
            "datasets": result.data or [],
        }

    except Exception as e:
        print("DATASET FETCH ERROR:", repr(e))

        raise HTTPException(
            status_code=400,
            detail=f"Unable to fetch datasets: {str(e)}"
        )

@app.get("/analysis/{dataset_id}")
async def analyze_saved_dataset(
    dataset_id: str,
    request: Request
):
    user_id = require_user(request)

    try:
        # -----------------------------------------
        # 1. Find dataset belonging to current user
        # -----------------------------------------

        dataset_result = (
            supabase
            .table("datasets")
            .select("*")
            .eq("id", dataset_id)
            .eq("user_id", user_id)
            .single()
            .execute()
        )

        dataset = dataset_result.data

        if not dataset:
            raise HTTPException(
                status_code=404,
                detail="Dataset not found."
            )

        storage_path = dataset.get("storage_path")

        if not storage_path:
            raise HTTPException(
                status_code=400,
                detail="Dataset storage path is missing."
            )

        # -----------------------------------------
        # 2. Download dataset from Supabase Storage
        # -----------------------------------------

        raw = (
            supabase
            .storage
            .from_("datasets")
            .download(storage_path)
        )

        filename = dataset["filename"].lower()

        # -----------------------------------------
        # 3. Read dataset
        # -----------------------------------------

        if filename.endswith(".csv"):
            df = pd.read_csv(io.BytesIO(raw))

        elif filename.endswith((".xlsx", ".xls")):
            df = pd.read_excel(io.BytesIO(raw))

        elif filename.endswith(".json"):
            df = pd.read_json(io.BytesIO(raw))

        else:
            raise HTTPException(
                status_code=400,
                detail="Unsupported dataset format."
            )

        # -----------------------------------------
        # 4. Basic statistics
        # -----------------------------------------

        rows = len(df)
        columns = len(df.columns)

        missing_values = int(
            df.isnull().sum().sum()
        )

        missing_percentage = round(
            (missing_values / df.size) * 100,
            2
        ) if df.size else 0

        duplicates = int(
            df.duplicated().sum()
        )

        # -----------------------------------------
        # 5. Column types
        # -----------------------------------------

        numerical_columns = df.select_dtypes(
            include=["number"]
        ).columns.tolist()

        categorical_columns = df.select_dtypes(
            include=["object", "category", "bool"]
        ).columns.tolist()

        datetime_columns = df.select_dtypes(
            include=["datetime"]
        ).columns.tolist()

        # -----------------------------------------
        # 6. Data quality
        # -----------------------------------------

        quality = 100

        quality -= min(
            missing_percentage,
            30
        )

        if rows > 0:
            duplicate_percentage = (
                duplicates / rows
            ) * 100

            quality -= min(
                duplicate_percentage,
                20
            )

        quality = max(
            round(quality, 2),
            0
        )

        # -----------------------------------------
        # 7. Column information
        # -----------------------------------------

        column_details = []

        for column in df.columns:

            column_details.append({
                "name": str(column),
                "type": str(df[column].dtype),
                "missing": int(
                    df[column].isnull().sum()
                ),
                "unique": int(
                    df[column].nunique()
                ),
            })

        # -----------------------------------------
        # 8. Numerical statistics
        # -----------------------------------------

        numerical_stats = []

        for column in numerical_columns:

            series = df[column]

            numerical_stats.append({
                "column": str(column),
                "mean": round(
                    float(series.mean()), 4
                ) if not series.empty else None,

                "median": round(
                    float(series.median()), 4
                ) if not series.empty else None,

                "min": round(
                    float(series.min()), 4
                ) if not series.empty else None,

                "max": round(
                    float(series.max()), 4
                ) if not series.empty else None,

                "std": round(
                    float(series.std()), 4
                ) if not series.empty else None,
            })

        # -----------------------------------------
        # 9. Categorical statistics
        # -----------------------------------------

        categorical_stats = []

        for column in categorical_columns:

            counts = (
                df[column]
                .value_counts(dropna=False)
                .head(10)
            )

            values = []

            for value, count in counts.items():

                if pd.isna(value):
                    value = "Missing"

                values.append({
                    "value": str(value),
                    "count": int(count)
                })

            categorical_stats.append({
                "column": str(column),
                "unique": int(
                    df[column].nunique()
                ),
                "top_values": values
            })

        # -----------------------------------------
        # 10. CHART DATA
        # -----------------------------------------

        charts = {}

        # -----------------------------------------
        # Missing values chart
        # -----------------------------------------

        missing_chart = []

        for column in df.columns:

         missing_count = int(
            df[column].isnull().sum()
            )

        missing_chart.append({
            "column": str(column),
            "missing": missing_count
        })

        charts["missing_values"] = missing_chart


        # -----------------------------------------
        # Numerical distribution data
        # -----------------------------------------

        distribution_charts = {}

        for column in numerical_columns:

            series = df[column].dropna()

            if series.empty:
                continue

        # Create 10 bins
        counts, bin_edges = pd.cut(
        series,
        bins=10,
        retbins=True
        )

        histogram = (
        series
        .groupby(counts, observed=False)
        .size()
        )

        distribution_charts[str(column)] = [
            {
                "range": str(interval),
                "count": int(count)
            }
            for interval, count in histogram.items()
        ]

        charts["distributions"] = distribution_charts


        # -----------------------------------------
        # Categorical chart data
        # -----------------------------------------

        categorical_charts = {}

        for column in categorical_columns:

            counts = (
            df[column]
            .value_counts(dropna=False)
            .head(10)
            )

        categorical_charts[str(column)] = [
            {
            "value": (
                "Missing"
                if pd.isna(value)
                else str(value)
            ),
            "count": int(count)
            }
            for value, count in counts.items()
        ]

        charts["categorical"] = categorical_charts


        # -----------------------------------------
        # Correlation matrix
        # -----------------------------------------

        correlation = None

        if len(numerical_columns) >= 2:

            corr = (
            df[numerical_columns]
            .corr()
            .round(4)
            )

        correlation = {
           "columns": corr.columns.tolist(),
           "values": corr.fillna(0).values.tolist()
        }

        charts["correlation"] = correlation


# -----------------------------------------
# Outlier data
# -----------------------------------------

        outlier_charts = {}

        for column in numerical_columns:

         series = df[column].dropna()

         if series.empty:
            continue

         q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)

        iqr = q3 - q1

        lower = q1 - (1.5 * iqr)
        upper = q3 + (1.5 * iqr)

        outlier_count = int(
        (
            (series < lower) |
            (series > upper)
        ).sum()
    )

        outlier_charts[str(column)] = {
        "q1": float(q1),
        "median": float(series.median()),
        "q3": float(q3),
        "lower": float(lower),
        "upper": float(upper),
        "outliers": outlier_count
    }

        charts["outliers"] = outlier_charts

        # -----------------------------------------
        # 10. Preview
        # -----------------------------------------

        preview = json.loads(
            df.head(10).to_json(
                orient="records",
                date_format="iso"
            )
        )

        return {
            "success": True,

            "dataset": {
                "id": dataset["id"],
                "filename": dataset["filename"],
                "rows": rows,
                "columns": columns,
                "missing_values": missing_values,
                "missing_percentage": missing_percentage,
                "duplicates": duplicates,
                "data_quality": quality,
            },

            "column_types": {
                "numerical": numerical_columns,
                "categorical": categorical_columns,
                "datetime": datetime_columns,
            },

            "columns": column_details,

            "numerical_stats": numerical_stats,

            "categorical_stats": categorical_stats,

            "preview": preview,
            "charts": charts,
        }

    except HTTPException:
        raise

    except Exception as e:

        print(
            "SAVED DATASET ANALYSIS ERROR:",
            repr(e)
        )

        raise HTTPException(
            status_code=400,
            detail=f"Unable to analyze dataset: {str(e)}"
        )