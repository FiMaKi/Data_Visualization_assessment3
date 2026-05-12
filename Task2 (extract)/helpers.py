"""
helpers.py

Small helper functions for the Global Sustainable Energy Dashboard.

This file contains logic that does not belong specifically to:
- data loading
- sidebar controls
- visual creation
- UI styling

Keeping these helper functions separate makes app.py shorter and easier to read.
"""

from __future__ import annotations

import pandas as pd


def get_latest_available_year_for_columns(
    df: pd.DataFrame,
    columns: list[str],
    selected_year: int,
) -> int | None:
    """
    Finds the latest year at or before the selected year where all required
    columns contain valid data.

    This is useful when the selected year does not contain complete data
    for a chart.

    Example:
    If the user selects 2020, but GDP and CO2 data are only complete up to 2019,
    the function returns 2019.

    Args:
        df:
            Dataframe containing a year column and the required data columns.

        columns:
            List of required columns that must contain non-missing values.

        selected_year:
            The year selected by the user.

    Returns:
        The latest available year as an integer, or None if no valid year exists.
    """
    if df.empty:
        return None

    if "year" not in df.columns:
        return None

    missing_columns = [
        column for column in columns
        if column not in df.columns
    ]

    if missing_columns:
        return None

    available_df = df[
        df["year"] <= selected_year
    ].dropna(
        subset=columns
    )

    if available_df.empty:
        available_df = df.dropna(
            subset=columns
        )

    if available_df.empty:
        return None

    return int(available_df["year"].max())