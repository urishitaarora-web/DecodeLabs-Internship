import io
import os
from typing import Any

import numpy as np
import pandas as pd

from fastapi import APIRouter, Depends, HTTPException
from clerk_auth import verify_clerk_token

from supabase import create_client, Client
from dotenv import load_dotenv


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv(
    "SUPABASE_SERVICE_ROLE_KEY"
)

if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
    raise RuntimeError(
        "Supabase credentials are missing."
    )


supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_SERVICE_ROLE_KEY
)

DATASET_BUCKET = "datasets"

router = APIRouter()


# ============================================================
# HELPERS
# ============================================================

def _user_id(user):
    """
    Extract Clerk user ID safely.
    """

    if isinstance(user, dict):
        return user.get("sub")

    return user


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

        if filename.endswith(
            (".xlsx", ".xls")
        ):
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
            detail=(
                f"Unable to read dataset: {str(e)}"
            ),
        )

    raise HTTPException(
        status_code=400,
        detail=(
            "Unsupported file type. "
            "Use CSV, XLSX, or JSON."
        ),
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
                detail="Dataset not found.",
            )

        return result.data

    except HTTPException:
        raise

    except Exception as e:

        print(
            "EDA DATASET LOOKUP ERROR:",
            repr(e),
        )

        raise HTTPException(
            status_code=400,
            detail="Unable to load dataset.",
        )


def _download_dataset(dataset):

    storage_path = dataset.get(
        "storage_path"
    )

    if not storage_path:

        raise HTTPException(
            status_code=400,
            detail=(
                "This dataset does not have "
                "a stored file."
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
            "EDA DATASET DOWNLOAD ERROR:",
            repr(e),
        )

        raise HTTPException(
            status_code=400,
            detail=(
                f"Unable to download dataset: {str(e)}"
            ),
        )


def _safe_value(value: Any):

    if value is None:
        return None

    if isinstance(
        value,
        (
            np.integer,
            np.int64,
            np.int32,
        ),
    ):
        return int(value)

    if isinstance(
        value,
        (
            np.floating,
            np.float64,
            np.float32,
        ),
    ):
        if np.isnan(value):
            return None

        return float(value)

    if isinstance(
        value,
        (
            pd.Timestamp,
        ),
    ):
        return value.isoformat()

    if pd.isna(value):
        return None

    return value


def _safe_records(
    records
):
    """
    Convert Pandas/Numpy values into
    JSON-safe Python values.
    """

    output = []

    for record in records:

        clean_record = {}

        for key, value in record.items():

            clean_record[str(key)] = (
                _safe_value(value)
            )

        output.append(clean_record)

    return output


# ============================================================
# NUMERIC DISTRIBUTIONS
# ============================================================

def _numeric_distributions(
    df: pd.DataFrame,
):

    result = []

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns

    for column in numeric_columns:

        series = df[column].dropna()

        if series.empty:
            continue

        # Keep chart size reasonable.
        bins = min(
            20,
            max(5, int(np.sqrt(len(series))))
        )

        try:

            counts, edges = np.histogram(
                series,
                bins=bins,
            )

            histogram = []

            for i in range(
                len(counts)
            ):

                histogram.append({
                    "bin": (
                        f"{edges[i]:.3g}"
                        f" – "
                        f"{edges[i + 1]:.3g}"
                    ),
                    "count": int(
                        counts[i]
                    ),
                    "start": float(
                        edges[i]
                    ),
                    "end": float(
                        edges[i + 1]
                    ),
                })

            result.append({
                "column": str(column),
                "count": int(
                    series.count()
                ),
                "sum": _safe_value(
                    series.sum()
                ),
                "mean": _safe_value(
                    series.mean()
                ),
                "median": _safe_value(
                    series.median()
                ),
                "min": _safe_value(
                    series.min()
                ),
                "max": _safe_value(
                    series.max()
                ),
                "std": _safe_value(
                    series.std()
                ),
                "variance": _safe_value(
                    series.var()
                ),
                "histogram": histogram,
            })

        except Exception as e:

            print(
                f"NUMERIC EDA ERROR [{column}]:",
                repr(e),
            )

    return result


# ============================================================
# CATEGORICAL DISTRIBUTIONS
# ============================================================

def _categorical_distributions(
    df: pd.DataFrame,
):

    result = []

    categorical_columns = df.select_dtypes(
        include=["object", "category", "bool"]
    ).columns

    for column in categorical_columns:

        series = df[column].dropna()

        if series.empty:
            continue

        value_counts = (
            series
            .astype(str)
            .value_counts()
            .head(15)
        )

        distribution = []

        for category, count in (
            value_counts.items()
        ):

            distribution.append({
                "category": str(category),
                "count": int(count),
            })

        result.append({
            "column": str(column),
            "unique": int(
                series.nunique()
            ),
            "top": (
                str(value_counts.index[0])
                if len(value_counts)
                else None
            ),
            "distribution": distribution,
        })

    return result


# ============================================================
# MISSING VALUES
# ============================================================

def _missing_values(
    df: pd.DataFrame,
):

    result = []

    total_rows = len(df)

    for column in df.columns:

        missing = int(
            df[column].isna().sum()
        )

        percentage = (
            (missing / total_rows) * 100
            if total_rows
            else 0
        )

        result.append({
            "column": str(column),
            "missing": missing,
            "percentage": round(
                percentage,
                2,
            ),
        })

    return result


# ============================================================
# OUTLIERS
# ============================================================

def _outlier_summary(
    df: pd.DataFrame,
):

    result = []

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns

    for column in numeric_columns:

        series = df[column].dropna()

        if series.empty:
            continue

        q1 = series.quantile(
            0.25
        )

        q3 = series.quantile(
            0.75
        )

        iqr = q3 - q1

        if pd.isna(iqr) or iqr == 0:

            result.append({
    "column": str(column),
    "count": 0,
    "percentage": 0,
    "min": _safe_value(series.min()),
    "q1": _safe_value(q1),
    "median": _safe_value(series.median()),
    "q3": _safe_value(q3),
    "max": _safe_value(series.max()),
    "lower_bound": _safe_value(q1),
    "upper_bound": _safe_value(q3),
})

            continue

        lower = (
            q1 - 1.5 * iqr
        )

        upper = (
            q3 + 1.5 * iqr
        )

        mask = (
            (series < lower)
            | (series > upper)
        )

        count = int(
            mask.sum()
        )

        percentage = (
            count / len(series) * 100
        )

        result.append({
            "column": str(column),
            "count": count,
            "percentage": round(
                percentage,
                2,
            ),
            "min": _safe_value(
                series.min()
            ),
            "q1": _safe_value(
                q1
            ),
             "median": _safe_value(
                series.median()
            ),
             "q3": _safe_value(
                 q3
            ),
             "max": _safe_value(
                series.max()
            ),
            "lower_bound": _safe_value(
                    lower
            ),
            "upper_bound": _safe_value(
                upper
            ),
        })

    return result


# ============================================================
# CORRELATION MATRIX
# ============================================================

def _correlation_matrix(
    df: pd.DataFrame,
):

    numeric_df = df.select_dtypes(
        include="number"
    )

    if numeric_df.shape[1] < 2:

        return {
            "columns": [],
            "matrix": [],
        }

    correlation = (
        numeric_df
        .corr()
        .round(4)
    )

    matrix = []

    for row_name in correlation.index:

        row = {
            "column": str(row_name)
        }

        for column_name in correlation.columns:

            row[str(column_name)] = (
                _safe_value(
                    correlation.loc[
                        row_name,
                        column_name
                    ]
                )
            )

        matrix.append(row)

    return {
        "columns": [
            str(column)
            for column in correlation.columns
        ],
        "matrix": matrix,
    }


# ============================================================
# DESCRIPTIVE STATISTICS
# ============================================================

def _statistics(
    df: pd.DataFrame,
):

    numeric_df = df.select_dtypes(
        include="number"
    )

    if numeric_df.empty:

        return []

    statistics = (
        numeric_df
        .describe()
        .transpose()
        .reset_index()
    )

    statistics = statistics.rename(
        columns={
            "index": "column"
        }
    )

    return _safe_records(
        statistics.to_dict(
            orient="records"
        )
    )

# ============================================================
# COGNIFY RECOMMENDATIONS
# ============================================================

def _cognify_recommendations(df: pd.DataFrame):

    recommendations = []

    missing_cells = int(
        df.isna().sum().sum()
    )

    duplicate_rows = int(
        df.duplicated().sum()
    )

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns

    categorical_columns = df.select_dtypes(
        include=["object", "category", "bool"]
    ).columns

    # Missing values
    if missing_cells > 0:
        recommendations.append({
            "type": "warning",
            "title": "Handle missing values",
            "message": (
                f"{missing_cells:,} missing cells were detected. "
                "Consider imputation or removal before model training."
            )
        })
    else:
        recommendations.append({
            "type": "success",
            "title": "No missing values",
            "message": (
                "The dataset is complete and does not require "
                "missing-value preprocessing."
            )
        })

    # Duplicate rows
    if duplicate_rows > 0:
        recommendations.append({
            "type": "warning",
            "title": "Remove duplicate records",
            "message": (
                f"{duplicate_rows:,} duplicate rows were detected. "
                "Consider removing them before analysis or training."
            )
        })

    # Numeric features
    if len(numeric_columns) > 0:
        recommendations.append({
            "type": "info",
            "title": "Scale numerical features",
            "message": (
                f"{len(numeric_columns)} numerical columns were detected. "
                "Feature scaling may improve performance for distance-based "
                "and gradient-based machine-learning models."
            )
        })

    # Categorical features
    if len(categorical_columns) > 0:
        recommendations.append({
            "type": "info",
            "title": "Encode categorical features",
            "message": (
                f"{len(categorical_columns)} categorical columns were detected. "
                "Consider one-hot encoding or another suitable encoding strategy "
                "before model training."
            )
        })

    return recommendations
# ============================================================
# EDA ENDPOINT
# ============================================================

@router.get(
    "/datasets/{dataset_id}/eda"
)
async def get_dataset_eda(
    dataset_id: str,
    user=Depends(
        verify_clerk_token
    ),
):

    user_id = _user_id(user)

    if not user_id:

        raise HTTPException(
            status_code=401,
            detail="Invalid authenticated user.",
        )

    # --------------------------------------------------------
    # 1. DATASET METADATA
    # --------------------------------------------------------

    dataset = _get_dataset_for_user(
        dataset_id,
        user_id,
    )

    # --------------------------------------------------------
    # 2. DOWNLOAD ORIGINAL DATASET
    # --------------------------------------------------------

    raw = _download_dataset(
        dataset
    )

    # --------------------------------------------------------
    # 3. LOAD DATAFRAME
    # --------------------------------------------------------

    df = _load_dataframe(
        dataset.get("filename"),
        raw,
    )

    if df.empty:

        raise HTTPException(
            status_code=400,
            detail="Dataset is empty.",
        )

    # --------------------------------------------------------
    # 4. COLUMN TYPES
    # --------------------------------------------------------

    numeric_columns = [
        str(column)
        for column in df.select_dtypes(
            include="number"
        ).columns
    ]

    categorical_columns = [
        str(column)
        for column in df.select_dtypes(
            include=[
                "object",
                "category",
                "bool",
            ]
        ).columns
    ]

    datetime_columns = [
        str(column)
        for column in df.select_dtypes(
            include=[
                "datetime",
                "datetimetz",
            ]
        ).columns
    ]

    # --------------------------------------------------------
    # 5. BUILD EDA
    # --------------------------------------------------------

    return {
        "status": "success",

        "dataset": {
            "id": dataset_id,
            "filename": dataset.get(
                "filename"
            ),
            "rows": int(
                len(df)
            ),
            "columns": int(
                len(df.columns)
            ),
        },

        "schema": {
            "numeric": numeric_columns,
            "categorical": categorical_columns,
            "datetime": datetime_columns,
        },

        "missing_values": (
            _missing_values(df)
        ),

        "numeric_distributions": (
            _numeric_distributions(df)
        ),

        "categorical_distributions": (
            _categorical_distributions(df)
        ),

        "outliers": (
            _outlier_summary(df)
        ),

        "correlation": (
            _correlation_matrix(df)
        ),

        "statistics": (
            _statistics(df)
        ),

        "recommendations": (
          _cognify_recommendations(df)
        ),

        "preview": _safe_records(
           df.head(10).to_dict(
             orient="records"
         )
        ),
        "summary": {
            "duplicate_rows": int(
                df.duplicated().sum()
            ),

            "missing_cells": int(
                df.isna().sum().sum()
            ),

            "numeric_columns": len(
                numeric_columns
            ),

            "categorical_columns": len(
                categorical_columns
            ),

            "datetime_columns": len(
                datetime_columns
            ),
        },
    }