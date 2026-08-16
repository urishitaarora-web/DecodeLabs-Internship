"""
Cognify Phase 2 - Preprocessing Engine

Core preprocessing logic for:
- Missing-value handling
- Duplicate removal
- Outlier detection

Pure functions operating on pandas DataFrames.
Framework-agnostic and reusable by the FastAPI backend.
"""

import pandas as pd
import numpy as np
from typing import Optional


# ---------------------------------------------------------------------------
# Missing value handling
# ---------------------------------------------------------------------------

def handle_missing_values(
    df: pd.DataFrame,
    strategy: str = "auto",
    columns: Optional[list] = None,
) -> tuple[pd.DataFrame, dict]:
    """
    Handle missing values in a DataFrame.

    Strategies:
        auto          -> numeric: median
                         categorical: mode
                         datetime: forward fill

        mean          -> numeric columns: mean

        median        -> numeric columns: median

        mode          -> all columns: most frequent value

        drop_rows     -> remove rows containing missing values

        drop_columns  -> remove columns with more than 50% missing values

        constant      -> numeric: 0
                         text/categorical: "Unknown"

    Args:
        df: Input pandas DataFrame.
        strategy: Missing-value handling strategy.
        columns: Optional list of columns to process.
                 None means all columns.

    Returns:
        cleaned DataFrame and preprocessing report.
    """

    valid_strategies = {
        "auto",
        "mean",
        "median",
        "mode",
        "drop_rows",
        "drop_columns",
        "constant",
    }

    if strategy not in valid_strategies:
        raise ValueError(
            f"Unknown missing-value strategy: {strategy}"
        )

    df = df.copy()
    missing_before = int(df.isna().sum().sum())

    target_cols = (
        columns
        if columns is not None
        else df.columns.tolist()
    )

    report = {
        "strategy": strategy,
        "columns_processed": [],
        "rows_before": len(df),
    }

    # -----------------------------------------------------------------------
    # Drop rows
    # -----------------------------------------------------------------------

    if strategy == "drop_rows":

        before = len(df)

        df = df.dropna(
            subset=target_cols
        ).reset_index(drop=True)

        report["rows_dropped"] = before - len(df)

    # -----------------------------------------------------------------------
    # Drop columns with >50% missing values
    # -----------------------------------------------------------------------

    elif strategy == "drop_columns":

        drop_cols = [
            column
            for column in target_cols
            if column in df.columns
            and df[column].isna().mean() > 0.50
        ]

        df = df.drop(
            columns=drop_cols
        )

        report["columns_dropped"] = drop_cols

    # -----------------------------------------------------------------------
    # Fill missing values
    # -----------------------------------------------------------------------

    else:

        for column in target_cols:

            if column not in df.columns:
                continue

            if df[column].isna().sum() == 0:
                continue

            series = df[column]

            is_numeric = pd.api.types.is_numeric_dtype(
                series
            )

            is_datetime = pd.api.types.is_datetime64_any_dtype(
                series
            )

            # ---------------------------------------------------------------
            # Automatic strategy
            # ---------------------------------------------------------------

            if strategy == "auto":

                if is_numeric:

                    fill_value = series.median()

                    if not pd.isna(fill_value):
                        df[column] = series.fillna(
                            fill_value
                        )

                elif is_datetime:

                    df[column] = series.ffill()

                    # If the first values are still missing,
                    # use backward fill.
                    df[column] = df[column].bfill()

                else:

                    mode = series.mode()

                    fill_value = (
                        mode.iloc[0]
                        if not mode.empty
                        else "Unknown"
                    )

                    df[column] = series.fillna(
                        fill_value
                    )

                report["columns_processed"].append(
                    column
                )

            # ---------------------------------------------------------------
            # Mean
            # ---------------------------------------------------------------

            elif strategy == "mean":

                if is_numeric:

                    fill_value = series.mean()

                    if not pd.isna(fill_value):
                        df[column] = series.fillna(
                            fill_value
                        )

                    report["columns_processed"].append(
                        column
                    )

            # ---------------------------------------------------------------
            # Median
            # ---------------------------------------------------------------

            elif strategy == "median":

                if is_numeric:

                    fill_value = series.median()

                    if not pd.isna(fill_value):
                        df[column] = series.fillna(
                            fill_value
                        )

                    report["columns_processed"].append(
                        column
                    )

            # ---------------------------------------------------------------
            # Mode
            # ---------------------------------------------------------------

            elif strategy == "mode":

                mode = series.mode()

                fill_value = (
                    mode.iloc[0]
                    if not mode.empty
                    else "Unknown"
                )

                df[column] = series.fillna(
                    fill_value
                )

                report["columns_processed"].append(
                    column
                )

            # ---------------------------------------------------------------
            # Constant
            # ---------------------------------------------------------------

            elif strategy == "constant":

                fill_value = (
                    0
                    if is_numeric
                    else "Unknown"
                )

                df[column] = series.fillna(
                    fill_value
                )

                report["columns_processed"].append(
                    column
                )

    # -----------------------------------------------------------------------
    # Final report
    # -----------------------------------------------------------------------

    report["rows_after"] = len(df)

    report["missing_before"] = missing_before

    report["missing_remaining"] = int(
        df.isna().sum().sum()
    )

    return df, report


# ---------------------------------------------------------------------------
# Duplicate removal
# ---------------------------------------------------------------------------

def remove_duplicates(
    df: pd.DataFrame,
    subset: Optional[list] = None,
    keep: str = "first",
) -> tuple[pd.DataFrame, dict]:
    """
    Remove duplicate rows.

    Args:
        df: Input pandas DataFrame.
        subset: Columns used to identify duplicates.
                None means all columns.
        keep:
            "first" -> keep first occurrence
            "last"  -> keep last occurrence
            False   -> remove all duplicate occurrences

    Returns:
        cleaned DataFrame and duplicate-removal report.
    """

    if keep not in {"first", "last", False}:
        raise ValueError(
            "keep must be 'first', 'last', or False"
        )

    df = df.copy()

    rows_before = len(df)

    duplicate_mask = df.duplicated(
        subset=subset,
        keep=keep
    )

    duplicate_count = int(
        duplicate_mask.sum()
    )

    df = (
        df.drop_duplicates(
            subset=subset,
            keep=keep
        )
        .reset_index(drop=True)
    )

    report = {
        "rows_before": rows_before,
        "rows_after": len(df),
        "duplicates_removed": duplicate_count,
        "subset": (
            subset
            if subset is not None
            else "all_columns"
        ),
        "keep": keep,
    }

    return df, report


# ---------------------------------------------------------------------------
# Outlier detection
# ---------------------------------------------------------------------------

def detect_outliers(
    df: pd.DataFrame,
    method: str = "iqr",
    columns: Optional[list] = None,
    action: str = "flag",
    z_threshold: float = 3.0,
    iqr_multiplier: float = 1.5,
) -> tuple[pd.DataFrame, dict]:
    """
    Detect and optionally handle numerical outliers.

    Methods:
        iqr
        zscore

    Actions:
        flag   -> add boolean outlier columns
        remove -> remove rows containing outliers
        cap    -> cap values at calculated bounds

    Args:
        df: Input pandas DataFrame.
        method: Detection method.
        columns: Numeric columns to check.
                 None means all numeric columns.
        action: How detected outliers should be handled.
        z_threshold: Z-score threshold.
        iqr_multiplier: IQR multiplier.

    Returns:
        processed DataFrame and outlier report.
    """

    valid_methods = {
        "iqr",
        "zscore",
    }

    valid_actions = {
        "flag",
        "remove",
        "cap",
    }

    if method not in valid_methods:
        raise ValueError(
            f"Unknown outlier method: {method}"
        )

    if action not in valid_actions:
        raise ValueError(
            f"Unknown outlier action: {action}"
        )

    df = df.copy()

    numeric_cols = (
        columns
        if columns is not None
        else df.select_dtypes(
            include=[np.number]
        ).columns.tolist()
    )

    outlier_summary = {}

    outlier_row_mask = pd.Series(
        False,
        index=df.index
    )

    for column in numeric_cols:

        if column not in df.columns:
            continue

        series = df[column]

        # Skip completely empty columns.
        if series.dropna().empty:
            continue

        # ---------------------------------------------------------------
        # IQR method
        # ---------------------------------------------------------------

        if method == "iqr":

            q1 = series.quantile(0.25)
            q3 = series.quantile(0.75)

            iqr = q3 - q1

            lower_bound = (
                q1 - iqr_multiplier * iqr
            )

            upper_bound = (
                q3 + iqr_multiplier * iqr
            )

        # ---------------------------------------------------------------
        # Z-score method
        # ---------------------------------------------------------------

        else:

            mean = series.mean()
            std = series.std()

            if pd.isna(std) or std == 0:
                continue

            lower_bound = (
                mean - z_threshold * std
            )

            upper_bound = (
                mean + z_threshold * std
            )

        # ---------------------------------------------------------------
        # Detect outliers
        # ---------------------------------------------------------------

        column_outlier_mask = (
            (series < lower_bound)
            | (series > upper_bound)
        )

        outlier_count = int(
            column_outlier_mask.sum()
        )

        outlier_summary[column] = {
            "lower_bound": round(
                float(lower_bound),
                4
            ),
            "upper_bound": round(
                float(upper_bound),
                4
            ),
            "outlier_count": outlier_count,
        }

        outlier_row_mask |= (
            column_outlier_mask
        )

        # ---------------------------------------------------------------
        # Flag
        # ---------------------------------------------------------------

        if action == "flag":

            df[
                f"is_outlier_{column}"
            ] = column_outlier_mask

        # ---------------------------------------------------------------
        # Cap / Winsorize
        # ---------------------------------------------------------------

        elif action == "cap":

            df[column] = series.clip(
                lower=lower_bound,
                upper=upper_bound
            )

    # -------------------------------------------------------------------
    # Remove outlier rows
    # -------------------------------------------------------------------

    rows_before = len(df)

    if action == "remove":

        df = (
            df.loc[~outlier_row_mask]
            .reset_index(drop=True)
        )

    rows_removed = (
        rows_before - len(df)
        if action == "remove"
        else 0
    )

    report = {
        "method": method,
        "action": action,
        "columns_checked": numeric_cols,
        "total_outlier_rows": int(
            outlier_row_mask.sum()
        ),
        "rows_removed": rows_removed,
        "per_column": outlier_summary,
    }

    return df, report


# ---------------------------------------------------------------------------
# Basic preprocessing pipeline
# ---------------------------------------------------------------------------

def run_basic_pipeline(
    df: pd.DataFrame,
    config: dict,
) -> tuple[pd.DataFrame, dict]:
    """
    Run the basic Cognify preprocessing pipeline.

    Pipeline order:

        1. Missing values
        2. Duplicate removal
        3. Outlier detection

    Example configuration:

        {
            "missing_values": {
                "enabled": True,
                "strategy": "auto"
            },

            "duplicates": {
                "enabled": True,
                "keep": "first"
            },

            "outliers": {
                "enabled": True,
                "method": "iqr",
                "action": "flag"
            }
        }

    Returns:
        processed DataFrame and complete preprocessing report.
    """

    df = df.copy()

    full_report = {
        "steps": [],
        "initial_shape": {
            "rows": len(df),
            "columns": len(df.columns),
        },
    }

    # -------------------------------------------------------------------
    # Step 1: Missing values
    # -------------------------------------------------------------------

    missing_config = config.get(
        "missing_values",
        {}
    )

    if missing_config.get(
        "enabled",
        True
    ):

        df, report = handle_missing_values(
            df,
            strategy=missing_config.get(
                "strategy",
                "auto"
            ),
        )

        full_report["steps"].append({
            "step": "missing_values",
            **report,
        })

    # -------------------------------------------------------------------
    # Step 2: Duplicate removal
    # -------------------------------------------------------------------

    duplicate_config = config.get(
        "duplicates",
        {}
    )

    if duplicate_config.get(
        "enabled",
        True
    ):

        df, report = remove_duplicates(
            df,
            keep=duplicate_config.get(
                "keep",
                "first"
            ),
        )

        full_report["steps"].append({
            "step": "duplicates",
            **report,
        })

    # -------------------------------------------------------------------
    # Step 3: Outlier detection
    # -------------------------------------------------------------------

    outlier_config = config.get(
        "outliers",
        {}
    )

    if outlier_config.get(
        "enabled",
        True
    ):

        df, report = detect_outliers(
            df,
            method=outlier_config.get(
                "method",
                "iqr"
            ),
            action=outlier_config.get(
                "action",
                "flag"
            ),
        )

        full_report["steps"].append({
            "step": "outliers",
            **report,
        })

    # -------------------------------------------------------------------
    # Final shape
    # -------------------------------------------------------------------

    full_report["final_shape"] = {
        "rows": len(df),
        "columns": len(df.columns),
    }

    full_report["final_missing_values"] = int(
        df.isna().sum().sum()
    )

    return df, full_report

