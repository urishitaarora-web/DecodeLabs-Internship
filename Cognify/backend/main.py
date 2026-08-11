from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

import pandas as pd
import io
import os
from dotenv import load_dotenv
from supabase import create_client, Client

from clerk_backend_api import Clerk
from clerk_backend_api import authenticate_request, AuthenticateRequestOptions

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
                "http://localhost:5173"
            ],
            accepts_token=["session_token"],
        ),
    )

    if not state.is_signed_in:
        raise HTTPException(
            status_code=401,
            detail="Authentication required."
        )

    return state.payload["sub"]

app = FastAPI(title="Cognify ML Backend")


# Allow React/Vite frontend to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
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
class DatasetSaveRequest(BaseModel):
    filename: str
    file_size: int
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
    dataset: DatasetSaveRequest,
    request: Request
):
    user_id = require_user(request)

    try:
        result = (
            supabase
            .table("datasets")
            .insert({
                "user_id": user_id,
                "filename": dataset.filename,
                "file_size": dataset.file_size,
                "rows": dataset.rows,
                "columns": dataset.columns,
                "missing_values": dataset.missing_values,
                "missing_percentage": dataset.missing_percentage,
                "duplicates": dataset.duplicates,
                "data_quality": dataset.data_quality,
                "column_types": dataset.column_types,
                "columns_info": dataset.columns_info,
                "status": dataset.status,
            })
            .execute()
        )

        return {
            "success": True,
            "dataset": result.data[0] if result.data else None,
        }

    except Exception as e:
        print("DATASET SAVE ERROR:", repr(e))

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