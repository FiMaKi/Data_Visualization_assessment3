"""
This file:
- finds the CSV dataset
- loads the data
- matches original column names to simpler internal names
- converts numeric columns safely
- creates derived columns when possible
- removes regional/income-group aggregate rows
- provides helper functions for available metrics
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
import streamlit as st

from config import (
    AGGREGATE_ENTITIES,
    COLUMN_ALIASES,
    DATA_FILE_CANDIDATES,
    LOCAL_TASK2_FOLDER,
    METRIC_LABELS,
)


# --------------------------------------------------
# Text and column matching helpers
# --------------------------------------------------

def normalise_text(value: str) -> str:
    """
    Standardises text for safer column-name matching.

    Example:
    'GDP per capita' and 'gdp_per_capita' become easier to compare.
    """
    return re.sub(r"[^a-z0-9]+", "", str(value).lower())


def find_dataset_file() -> Path:
    
    app_folder = Path(__file__).resolve().parent

    folders_to_check = [
        app_folder,
        LOCAL_TASK2_FOLDER,
    ]

    for folder in folders_to_check:
        for file_name in DATA_FILE_CANDIDATES:
            candidate = folder / file_name

            if candidate.exists():
                return candidate

    searched_locations = "\n".join(
        str(folder / file_name)
        for folder in folders_to_check
        for file_name in DATA_FILE_CANDIDATES
    )

    raise FileNotFoundError(
        "Could not find the sustainable energy CSV file.\n\n"
        "Make sure the CSV file is in the same folder as app.py and named:\n"
        "global-data-on-sustainable-energy.csv\n\n"
        f"Searched these locations:\n{searched_locations}"
    )


def find_column(df: pd.DataFrame, aliases: List[str]) -> Optional[str]:
    """
    Finds a matching real column name in the dataset using a list of aliases.

    This makes the dashboard more robust if the CSV uses slightly different
    column names.
    """
    normalised_columns = {
        normalise_text(column): column
        for column in df.columns
    }

    for alias in aliases:
        normalised_alias = normalise_text(alias)

        if normalised_alias in normalised_columns:
            return normalised_columns[normalised_alias]

    return None


def rename_columns(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, str], List[str]]:
    """
    Renames original dataset columns to shorter internal names.

    Returns:
    - renamed dataframe
    - dictionary showing which original columns were matched
    - list of optional internal columns that were not found
    """
    rename_map = {}
    matched_columns = {}
    missing_internal_columns = []

    for internal_name, aliases in COLUMN_ALIASES.items():
        original_column = find_column(df, aliases)

        if original_column is not None:
            rename_map[original_column] = internal_name
            matched_columns[internal_name] = original_column
        else:
            missing_internal_columns.append(internal_name)

    renamed_df = df.rename(columns=rename_map)

    return renamed_df, matched_columns, missing_internal_columns


# --------------------------------------------------
# Data cleaning helpers
# --------------------------------------------------

def convert_to_numeric(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    """
    Converts selected columns to numeric values.

    Handles:
    - commas in large numbers
    - spaces
    - percentage signs
    - currency signs
    - invalid values
    """
    cleaned_df = df.copy()

    for column in columns:
        if column in cleaned_df.columns:
            cleaned_df[column] = (
                cleaned_df[column]
                .astype(str)
                .str.replace(",", "", regex=False)
                .str.replace("%", "", regex=False)
                .str.replace("$", "", regex=False)
                .str.replace(" ", "", regex=False)
            )

            cleaned_df[column] = pd.to_numeric(
                cleaned_df[column],
                errors="coerce",
            )

    return cleaned_df


def add_derived_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds useful derived columns when the required source columns exist.

    Derived columns:
    - estimated_population
    - co2_per_capita, if missing or partly missing
    - low_carbon_electricity_pct, if missing and electricity source data exists
    """
    output = df.copy()

    # --------------------------------------------------
    # Estimated population
    # --------------------------------------------------
    # Population is estimated from population density × land area.
    # This is only used as a fallback for bubble size or CO2 calculations
    # when direct population data is not available.

    if "population_density" in output.columns and "land_area" in output.columns:
        output["estimated_population"] = (
            output["population_density"] * output["land_area"]
        )

        output.loc[
            output["estimated_population"] <= 0,
            "estimated_population",
        ] = np.nan

    # --------------------------------------------------
    # CO2 per capita fallback
    # --------------------------------------------------
    # If the dataset does not contain CO2 per capita, or contains missing values,
    # calculate it from total CO2 emissions and estimated population where possible.
    #
    # co2_total_kt is kilotonnes.
    # 1 kilotonne = 1000 metric tons.
    # metric tons per person = (kilotonnes × 1000) / population.

    if "co2_total_kt" in output.columns and "estimated_population" in output.columns:
        calculated_co2_per_capita = (
            output["co2_total_kt"] * 1000
        ) / output["estimated_population"]

        if "co2_per_capita" not in output.columns:
            output["co2_per_capita"] = calculated_co2_per_capita
        else:
            output["co2_per_capita"] = output["co2_per_capita"].fillna(
                calculated_co2_per_capita
            )

    # --------------------------------------------------
    # Low-carbon electricity percentage fallback
    # --------------------------------------------------
    # Low-carbon electricity = nuclear electricity + renewable electricity.
    # This calculation is only used if the dataset does not already contain
    # a low-carbon electricity percentage column.

    electricity_columns = [
        "electricity_fossil_twh",
        "electricity_nuclear_twh",
        "electricity_renewables_twh",
    ]

    if (
        "low_carbon_electricity_pct" not in output.columns
        and all(column in output.columns for column in electricity_columns)
    ):
        total_electricity = (
            output["electricity_fossil_twh"]
            + output["electricity_nuclear_twh"]
            + output["electricity_renewables_twh"]
        )

        low_carbon_electricity = (
            output["electricity_nuclear_twh"]
            + output["electricity_renewables_twh"]
        )

        output["low_carbon_electricity_pct"] = np.where(
            total_electricity > 0,
            (low_carbon_electricity / total_electricity) * 100,
            np.nan,
        )

    return output


# --------------------------------------------------
# Main data loading function
# --------------------------------------------------

@st.cache_data(show_spinner=False)
def load_and_clean_data() -> Tuple[pd.DataFrame, Dict[str, str], List[str], Path]:
    """
    Loads and cleans the sustainable energy dataset.

    Streamlit caches this function so the app does not reload the CSV every time
    a filter changes.

    Returns:
    - cleaned dataframe
    - matched column dictionary
    - missing optional columns
    - dataset path
    """
    data_path = find_dataset_file()

    raw_df = pd.read_csv(data_path)
    raw_df.columns = raw_df.columns.str.strip()

    df, matched_columns, missing_columns = rename_columns(raw_df)

    # --------------------------------------------------
    # Validate essential columns
    # --------------------------------------------------

    essential_columns = ["country", "year"]

    missing_essential = [
        column for column in essential_columns
        if column not in df.columns
    ]

    if missing_essential:
        raise ValueError(
            f"The dataset is missing essential columns: {missing_essential}. "
            "The dashboard needs at least country/entity and year."
        )

    # --------------------------------------------------
    # Basic cleaning
    # --------------------------------------------------

    df["country"] = df["country"].astype(str).str.strip()
    df["year"] = pd.to_numeric(df["year"], errors="coerce")

    df = df.dropna(subset=["country", "year"])
    df["year"] = df["year"].astype(int)

    # --------------------------------------------------
    # Numeric conversion
    # --------------------------------------------------

    numeric_columns = [
        column for column in COLUMN_ALIASES.keys()
        if column not in ["country", "year"]
    ]

    df = convert_to_numeric(df, numeric_columns)

    # --------------------------------------------------
    # Derived columns
    # --------------------------------------------------

    df = add_derived_columns(df)

    # --------------------------------------------------
    # Remove rows with no usable metric data
    # --------------------------------------------------

    available_metric_columns = [
        column for column in METRIC_LABELS.keys()
        if column in df.columns
    ]

    if available_metric_columns:
        df = df.dropna(
            subset=available_metric_columns,
            how="all",
        )

    return df, matched_columns, missing_columns, data_path


# --------------------------------------------------
# Country-level filtering
# --------------------------------------------------

def remove_aggregate_entities(df: pd.DataFrame) -> pd.DataFrame:
    """
    Removes broad region, income-group, or aggregate entities.

    If latitude and longitude are available, rows without coordinates are also
    removed because they are often regional or aggregate entities rather than
    individual countries.

    This makes maps, rankings, averages, and country comparisons more reliable.
    """
    cleaned = df.copy()

    cleaned = cleaned[
        ~cleaned["country"].isin(AGGREGATE_ENTITIES)
    ].copy()

    if "latitude" in cleaned.columns and "longitude" in cleaned.columns:
        cleaned = cleaned.dropna(
            subset=["latitude", "longitude"]
        ).copy()

    return cleaned


# --------------------------------------------------
# Metric availability helper
# --------------------------------------------------

def available_metrics(df: pd.DataFrame, metric_names: List[str]) -> List[str]:
    """
    Returns metrics that:
    - exist in the dataframe
    - contain at least one non-missing value

    This prevents the dashboard from showing sidebar metric options that cannot
    produce a chart.
    """
    return [
        metric for metric in metric_names
        if metric in df.columns and df[metric].notna().any()
    ]