"""
sidebar.py

Contains all sidebar-related logic for the Global Sustainable Energy Dashboard.

This file handles:
- light/dark theme toggle
- year filters
- country quick-pick groups
- continent selection
- metric selectors
- reset filters button

The goal is to keep app.py shorter and easier to read.
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

from config import (
    COUNTRY_GROUPS,
    COUNTRY_NAME_ALIASES,
    COUNTRY_TREND_METRIC_OPTIONS,
    CONTINENT_GROUPS,
    DEFAULT_CONTINENT,
    DEFAULT_COUNTRIES,
    DEFAULT_COUNTRY_GROUP,
    DEFAULT_COUNTRY_TREND_METRIC,
    DEFAULT_GLOBAL_TREND_METRIC,
    DEFAULT_MAP_METRIC,
    DEFAULT_RANKING_METRIC,
    DEFAULT_SELECTED_YEAR,
    DEFAULT_THEME_MODE,
    DEFAULT_TOP_N_RANKING,
    DEFAULT_TREND_END_YEAR,
    DEFAULT_TREND_START_YEAR,
    GLOBAL_TREND_METRIC_OPTIONS,
    MAP_METRIC_OPTIONS,
    METRIC_LABELS,
    RANKING_METRIC_OPTIONS,
)

from data_loader import available_metrics


# --------------------------------------------------
# Theme control
# --------------------------------------------------

def initialise_theme() -> str:
    """
    Creates the light/dark theme toggle in the sidebar.

    Returns:
        The currently selected theme mode: "Light" or "Dark".
    """
    if "theme_mode" not in st.session_state:
        st.session_state["theme_mode"] = DEFAULT_THEME_MODE

    theme_button_label = (
        "🌙 Switch to dark theme"
        if st.session_state["theme_mode"] == "Light"
        else "☀️ Switch to light theme"
    )

    if st.sidebar.button(
        theme_button_label,
        use_container_width=True,
        key="theme_toggle_button",
    ):
        st.session_state["theme_mode"] = (
            "Dark"
            if st.session_state["theme_mode"] == "Light"
            else "Light"
        )

        st.rerun()

    return st.session_state["theme_mode"]


# --------------------------------------------------
# Country helper functions
# --------------------------------------------------

def resolve_country_name(
    country_name: str,
    all_available_countries: list[str],
) -> str | None:
    """
    Finds the matching country name from the dataset.

    This allows quick-pick groups to use common names such as Russia,
    even if the CSV uses another name such as Russian Federation.
    """
    if country_name in all_available_countries:
        return country_name

    aliases = COUNTRY_NAME_ALIASES.get(country_name, [])

    for alias in aliases:
        if alias in all_available_countries:
            return alias

    return None


def resolve_country_group(
    country_names: list[str],
    all_available_countries: list[str],
) -> tuple[list[str], list[str]]:
    """
    Resolves a list of country names against the available countries in the dataset.

    Returns:
    - countries found in the dataset
    - countries not found in the dataset
    """
    resolved_countries = []
    missing_countries = []

    for country_name in country_names:
        resolved_name = resolve_country_name(
            country_name=country_name,
            all_available_countries=all_available_countries,
        )

        if resolved_name is None:
            missing_countries.append(country_name)
        else:
            resolved_countries.append(resolved_name)

    resolved_countries = sorted(
        list(dict.fromkeys(resolved_countries))
    )

    return resolved_countries, missing_countries


# --------------------------------------------------
# Sidebar builder
# --------------------------------------------------

def build_sidebar(country_df: pd.DataFrame) -> dict:
    """
    Builds the complete sidebar and returns all selected values.

    Args:
        country_df:
            Cleaned country-level dataframe.

    Returns:
        Dictionary containing all sidebar selections.
    """

    # --------------------------------------------------
    # Sidebar title
    # --------------------------------------------------

    st.sidebar.title("Filters")

    st.sidebar.caption(
        "Use the controls below to choose the year, countries, and metrics used in the dashboard."
    )

    # --------------------------------------------------
    # Time filters
    # --------------------------------------------------

    with st.sidebar.expander("Time", expanded=False):
        min_year = int(country_df["year"].min())
        max_year = int(country_df["year"].max())

        default_selected_year = (
            DEFAULT_SELECTED_YEAR
            if min_year <= DEFAULT_SELECTED_YEAR <= max_year
            else max_year
        )

        default_trend_start = max(
            DEFAULT_TREND_START_YEAR,
            min_year,
        )

        default_trend_end = min(
            DEFAULT_TREND_END_YEAR,
            max_year,
        )

        if default_trend_start > default_trend_end:
            default_trend_start = min_year
            default_trend_end = max_year

        selected_year = st.slider(
            "Selected year",
            min_value=min_year,
            max_value=max_year,
            value=default_selected_year,
            step=1,
            key="selected_year",
            help=(
                "Controls the single-year charts, overview cards, map, ranking, "
                "and electricity mix."
            ),
        )

        selected_year_range = st.slider(
            "Trend year range",
            min_value=min_year,
            max_value=max_year,
            value=(default_trend_start, default_trend_end),
            step=1,
            key="selected_year_range",
            help="Controls the time range used in the line charts.",
        )

    # --------------------------------------------------
    # Geography filters
    # --------------------------------------------------

    all_countries = sorted(
        country_df["country"].dropna().unique()
    )

    with st.sidebar.expander("Geography", expanded=False):
        country_group_options = [
            "Top 5",
            "Favorites",
            "BRICS",
            "NATO",
            "G7",
        ]

        default_country_group_index = (
            country_group_options.index(DEFAULT_COUNTRY_GROUP)
            if DEFAULT_COUNTRY_GROUP in country_group_options
            else 0
        )

        selected_country_group = st.selectbox(
            "Country quick pick",
            options=country_group_options,
            index=default_country_group_index,
            key="selected_country_group",
            help=(
                "Selects a preset group of countries. "
                "Top 5 is the default group."
            ),
        )

        continent_options = [
            "None",
            "Africa",
            "Antarctica",
            "Asia",
            "Europe",
            "North America",
            "Oceania",
            "South America",
        ]

        default_continent_index = (
            continent_options.index(DEFAULT_CONTINENT)
            if DEFAULT_CONTINENT in continent_options
            else 0
        )

        selected_continent = st.selectbox(
            "Continents",
            options=continent_options,
            index=default_continent_index,
            key="selected_continent",
            help=(
                "Selects countries from a continent. "
                "If a continent is selected, it overrides the country quick pick."
            ),
        )

        if selected_continent != "None":
            default_countries, missing_group_countries = resolve_country_group(
                country_names=CONTINENT_GROUPS[selected_continent],
                all_available_countries=all_countries,
            )

            active_country_source = f"Continent: {selected_continent}"

        else:
            default_countries, missing_group_countries = resolve_country_group(
                country_names=COUNTRY_GROUPS[selected_country_group],
                all_available_countries=all_countries,
            )

            active_country_source = f"Quick pick: {selected_country_group}"

        if not default_countries and selected_continent == "None":
            default_countries = [
                country for country in DEFAULT_COUNTRIES
                if country in all_countries
            ]

        if not default_countries:
            default_countries = all_countries[:5]

        selected_countries = st.multiselect(
            "Countries for comparison",
            options=all_countries,
            default=default_countries,
            key=f"country_selector_{selected_country_group}_{selected_continent}",
            help=(
                "These countries are used in selected-country comparison charts. "
                "Some sections also have their own checkbox to use all countries."
            ),
        )

        st.caption(
            f"Active selection: {active_country_source}"
        )

        if selected_continent != "None":
            st.caption(
                "The continent selector overrides the country quick pick."
            )

        if missing_group_countries:
            st.caption(
                "Not found in dataset: "
                + ", ".join(missing_group_countries)
            )

        if not selected_countries:
            st.warning(
                "No countries are currently selected. Some comparison charts may not display."
            )

    # --------------------------------------------------
    # Metric filters
    # --------------------------------------------------

    with st.sidebar.expander("Metrics", expanded=False):
        map_metric_options = available_metrics(
            country_df,
            MAP_METRIC_OPTIONS,
        )

        if not map_metric_options:
            st.error("No suitable map metrics were found in the dataset.")
            st.stop()

        default_map_metric_index = (
            map_metric_options.index(DEFAULT_MAP_METRIC)
            if DEFAULT_MAP_METRIC in map_metric_options
            else 0
        )

        selected_map_metric = st.selectbox(
            "Map colour metric",
            options=map_metric_options,
            index=default_map_metric_index,
            format_func=lambda metric: METRIC_LABELS.get(metric, metric),
            key="selected_map_metric",
            help="Controls the colour scale used in the world map.",
        )

        global_trend_metric_options = available_metrics(
            country_df,
            GLOBAL_TREND_METRIC_OPTIONS,
        )

        if not global_trend_metric_options:
            st.error("No suitable global trend metrics were found in the dataset.")
            st.stop()

        default_global_trend_index = (
            global_trend_metric_options.index(DEFAULT_GLOBAL_TREND_METRIC)
            if DEFAULT_GLOBAL_TREND_METRIC in global_trend_metric_options
            else 0
        )

        selected_global_trend_metric = st.selectbox(
            "Global trend metric",
            options=global_trend_metric_options,
            index=default_global_trend_index,
            format_func=lambda metric: METRIC_LABELS.get(metric, metric),
            key="selected_global_trend_metric",
            help="Controls the metric shown in the country-level trend chart.",
        )

        country_trend_metric_options = available_metrics(
            country_df,
            COUNTRY_TREND_METRIC_OPTIONS,
        )

        if not country_trend_metric_options:
            st.error("No suitable country trend metrics were found in the dataset.")
            st.stop()

        default_country_trend_index = (
            country_trend_metric_options.index(DEFAULT_COUNTRY_TREND_METRIC)
            if DEFAULT_COUNTRY_TREND_METRIC in country_trend_metric_options
            else 0
        )

        selected_country_trend_metric = st.selectbox(
            "Country comparison metric",
            options=country_trend_metric_options,
            index=default_country_trend_index,
            format_func=lambda metric: METRIC_LABELS.get(metric, metric),
            key="selected_country_trend_metric",
            help="Controls the metric shown in the selected-country comparison line chart.",
        )

        ranking_metric_options = available_metrics(
            country_df,
            RANKING_METRIC_OPTIONS,
        )

        if not ranking_metric_options:
            st.error("No suitable ranking metrics were found in the dataset.")
            st.stop()

        default_ranking_index = (
            ranking_metric_options.index(DEFAULT_RANKING_METRIC)
            if DEFAULT_RANKING_METRIC in ranking_metric_options
            else 0
        )

        selected_ranking_metric = st.selectbox(
            "Ranking metric",
            options=ranking_metric_options,
            index=default_ranking_index,
            format_func=lambda metric: METRIC_LABELS.get(metric, metric),
            key="selected_ranking_metric",
            help="Controls which metric is used in the country ranking chart.",
        )

        top_n = st.slider(
            "Number of countries in ranking",
            min_value=5,
            max_value=20,
            value=DEFAULT_TOP_N_RANKING,
            step=1,
            key="top_n_ranking",
            help="Controls how many countries are displayed in the ranking chart.",
        )

    # --------------------------------------------------
    # Other options
    # --------------------------------------------------

    with st.sidebar.expander("Options", expanded=False):
        use_log_gdp_axis = st.checkbox(
            "Use logarithmic GDP axis in scatter plot",
            value=True,
            key="use_log_gdp_axis",
            help=(
                "Useful because GDP per capita varies greatly between countries. "
                "A logarithmic axis can make the scatter plot easier to read."
            ),
        )

        show_cleaning_details = st.checkbox(
            "Show data checks and column matching",
            value=False,
            key="show_cleaning_details",
            help=(
                "Shows technical details about matched columns, missing optional columns, "
                "dataset size, and current sidebar selections."
            ),
        )

    # --------------------------------------------------
    # Reset filters button
    # --------------------------------------------------

    if st.sidebar.button(
        "↻ Reset filters",
        use_container_width=True,
        key="reset_filters_button",
    ):
        current_theme = st.session_state.get(
            "theme_mode",
            DEFAULT_THEME_MODE,
        )

        st.session_state.clear()

        st.session_state["theme_mode"] = current_theme

        st.rerun()

    # --------------------------------------------------
    # Return selected values
    # --------------------------------------------------

    return {
        "min_year": min_year,
        "max_year": max_year,
        "selected_year": selected_year,
        "selected_year_range": selected_year_range,
        "selected_country_group": selected_country_group,
        "selected_continent": selected_continent,
        "selected_countries": selected_countries,
        "selected_map_metric": selected_map_metric,
        "selected_global_trend_metric": selected_global_trend_metric,
        "selected_country_trend_metric": selected_country_trend_metric,
        "selected_ranking_metric": selected_ranking_metric,
        "top_n": top_n,
        "use_log_gdp_axis": use_log_gdp_axis,
        "show_cleaning_details": show_cleaning_details,
    }