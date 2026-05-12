"""
This file contains:
- dashboard CSS styling
- light/dark theme support
- number formatting helpers
- KPI card helpers
- reusable section headers
"""

from __future__ import annotations

from typing import Optional

import pandas as pd
import streamlit as st


# --------------------------------------------------
# Dashboard styling
# --------------------------------------------------

def inject_custom_css(theme_mode: str = "Light") -> None:
    """
    Adds dashboard styling.

    The dashboard layout stays the same in light and dark mode.
    Only the colour palette changes.
    """
    if theme_mode == "Dark":
        background = "#0B0F17"
        sidebar_background = "#1F2430"
        card_background = "#111827"
        border_colour = "#374151"
        text_colour = "#F9FAFB"
        muted_text = "#A3AAB8"
        accent_colour = "#60A5FA"
        button_background = "#252B38"
        button_hover = "#334155"
        input_background = "#111827"

    else:
        background = "#F6F8FB"
        sidebar_background = "#FFFFFF"
        card_background = "#FFFFFF"
        border_colour = "#E5E7EB"
        text_colour = "#111827"
        muted_text = "#6B7280"
        accent_colour = "#2563EB"
        button_background = "#FFFFFF"
        button_hover = "#EFF6FF"
        input_background = "#FFFFFF"

    st.markdown(
        f"""
        <style>
        /* --------------------------------------------------
           Main app
        -------------------------------------------------- */

        .stApp {{
            background-color: {background};
            color: {text_colour};
        }}

        .block-container {{
            padding-top: 1.4rem;
            padding-bottom: 2rem;
            max-width: 1180px;
        }}

        h1, h2, h3, h4, h5, h6 {{
            color: {text_colour};
            letter-spacing: -0.02em;
        }}

        p, label, span, div {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        }}

        /* --------------------------------------------------
           Sidebar
        -------------------------------------------------- */

        section[data-testid="stSidebar"] {{
            background-color: {sidebar_background};
            border-right: 1px solid {border_colour};
        }}

        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] span {{
            color: {text_colour};
        }}

        section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {{
            color: {muted_text};
            line-height: 1.45;
        }}

        section[data-testid="stSidebar"] details {{
            background-color: {button_background};
            border: 1px solid {border_colour};
            border-radius: 12px;
            margin-bottom: 0.75rem;
            box-shadow: 0px 1px 3px rgba(15, 23, 42, 0.06);
        }}

        section[data-testid="stSidebar"] summary {{
            padding: 0.75rem 0.9rem;
            font-weight: 700;
            color: {text_colour};
        }}

        section[data-testid="stSidebar"] details div[data-testid="stVerticalBlock"] {{
            padding-left: 0.15rem;
            padding-right: 0.15rem;
        }}

        /* Sidebar buttons */
        section[data-testid="stSidebar"] button {{
            border-radius: 10px;
            border: 1px solid {border_colour};
            background-color: {button_background};
            color: {text_colour};
            font-weight: 650;
        }}

        section[data-testid="stSidebar"] button:hover {{
            border-color: {accent_colour};
            color: {accent_colour};
            background-color: {button_hover};
        }}

        /* --------------------------------------------------
           Main cards and bordered containers
        -------------------------------------------------- */

        div[data-testid="stVerticalBlockBorderWrapper"] {{
            border-color: {border_colour} !important;
            border-radius: 16px !important;
            background-color: {card_background};
            box-shadow: 0px 1px 6px rgba(15, 23, 42, 0.07);
        }}

        /* --------------------------------------------------
           KPI cards
        -------------------------------------------------- */

        .kpi-card {{
            background-color: {card_background};
            border: 1px solid {border_colour};
            border-radius: 14px;
            padding: 1rem;
            min-height: 130px;
            box-shadow: 0px 1px 6px rgba(15, 23, 42, 0.07);
        }}

        .kpi-title {{
            color: {muted_text};
            font-size: 0.9rem;
            font-weight: 650;
            line-height: 1.25;
            margin-bottom: 0.75rem;
        }}

        .kpi-value {{
            color: {text_colour};
            font-size: 1.9rem;
            font-weight: 800;
            line-height: 1.1;
            margin-bottom: 0.8rem;
            letter-spacing: -0.03em;
        }}

        .kpi-note {{
            color: {muted_text};
            font-size: 0.8rem;
            line-height: 1.25;
        }}

        /* --------------------------------------------------
           Streamlit metric fallback styling
        -------------------------------------------------- */

        div[data-testid="stMetric"] {{
            background-color: {card_background};
            padding: 1rem;
            border-radius: 14px;
            border: 1px solid {border_colour};
            box-shadow: 0px 1px 6px rgba(15, 23, 42, 0.07);
        }}

        div[data-testid="stMetricLabel"] {{
            color: {muted_text};
            font-weight: 650;
        }}

        div[data-testid="stMetricValue"] {{
            color: {text_colour};
            font-weight: 800;
        }}

        /* --------------------------------------------------
           Section headers
        -------------------------------------------------- */

        .section-header {{
            font-size: 1.35rem;
            font-weight: 800;
            color: {text_colour};
            margin-top: 1.6rem;
            margin-bottom: 0.35rem;
            letter-spacing: -0.02em;
        }}

        .section-note {{
            font-size: 0.94rem;
            color: {muted_text};
            margin-bottom: 0.9rem;
            line-height: 1.45;
        }}

        /* --------------------------------------------------
           Captions and alerts
        -------------------------------------------------- */

        div[data-testid="stCaptionContainer"] {{
            color: {muted_text};
        }}

        div[data-testid="stAlert"] {{
            border-radius: 12px;
        }}

        /* --------------------------------------------------
           Inputs
        -------------------------------------------------- */

        div[data-baseweb="select"] > div {{
            border-radius: 10px;
            border-color: {border_colour};
            background-color: {input_background};
        }}

        input {{
            border-radius: 10px;
            background-color: {input_background};
            color: {text_colour};
        }}

        textarea {{
            background-color: {input_background};
            color: {text_colour};
        }}

        /* --------------------------------------------------
           Dataframes
        -------------------------------------------------- */

        div[data-testid="stDataFrame"] {{
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid {border_colour};
        }}

        /* --------------------------------------------------
           Plotly chart cards
        -------------------------------------------------- */

        div[data-testid="stPlotlyChart"] {{
            background-color: {card_background};
            border: 1px solid {border_colour};
            border-radius: 16px;
            padding: 0.75rem;
            box-shadow: 0px 1px 6px rgba(15, 23, 42, 0.07);
            margin-bottom: 1.2rem;
        }}

        /* --------------------------------------------------
           Links
        -------------------------------------------------- */

        a {{
            color: {accent_colour};
        }}

        </style>
        """,
        unsafe_allow_html=True,
    )


# --------------------------------------------------
# Number helpers
# --------------------------------------------------

def format_number(
    value: Optional[float],
    decimals: int = 1,
    suffix: str = "",
) -> str:
    """
    Formats numbers for KPI cards.

    Examples:
    - 98.234 with suffix="%" becomes "98.2%"
    - 1500000 becomes "1.5M"
    """
    if value is None or pd.isna(value):
        return "N/A"

    if abs(value) >= 1_000_000_000:
        return f"{value / 1_000_000_000:.{decimals}f}B{suffix}"

    if abs(value) >= 1_000_000:
        return f"{value / 1_000_000:.{decimals}f}M{suffix}"

    if abs(value) >= 1_000:
        return f"{value / 1_000:.{decimals}f}K{suffix}"

    return f"{value:.{decimals}f}{suffix}"


def safe_mean(df: pd.DataFrame, column: str) -> Optional[float]:
    """
    Calculates a simple country-level mean safely.

    This is not population-weighted.
    Each country contributes equally.
    """
    if column not in df.columns:
        return None

    values = df[column].dropna()

    if values.empty:
        return None

    return float(values.mean())


def latest_available_country_mean(
    full_df: pd.DataFrame,
    column: str,
    selected_year: int,
) -> tuple[Optional[float], Optional[int]]:
    """
    Finds the latest available country-level mean for a column.

    This is useful when the selected year has missing values,
    for example when CO2 values are not available for the newest year.
    """
    if full_df is None:
        return None, None

    if column not in full_df.columns:
        return None, None

    if "year" not in full_df.columns:
        return None, None

    available_data = full_df[
        (full_df["year"] <= selected_year)
        & (full_df[column].notna())
    ].copy()

    if available_data.empty:
        available_data = full_df[
            full_df[column].notna()
        ].copy()

    if available_data.empty:
        return None, None

    latest_year = int(available_data["year"].max())

    latest_values = available_data[
        available_data["year"] == latest_year
    ][column].dropna()

    if latest_values.empty:
        return None, None

    return float(latest_values.mean()), latest_year


# --------------------------------------------------
# Reusable UI components
# --------------------------------------------------

def section_header(title: str, note: Optional[str] = None) -> None:
    """
    Displays a styled section header.
    """
    st.markdown(
        f"<div class='section-header'>{title}</div>",
        unsafe_allow_html=True,
    )

    if note:
        st.markdown(
            f"<div class='section-note'>{note}</div>",
            unsafe_allow_html=True,
        )


def show_chart_explanation(question: str, encoding: str) -> None:
    """
    Adds a short explanation below a chart.

    This function is kept for flexibility, but the current dashboard may not use it
    if the design is kept more minimal.
    """
    st.caption(
        f"**Question:** {question}  \n"
        f"**Encoding:** {encoding}"
    )


def kpi_card(
    title: str,
    value: str,
    note: str = "",
) -> None:
    """
    Creates a readable KPI card.

    The card uses CSS classes from inject_custom_css().
    """
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">{title}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_kpi_cards(
    year_df: pd.DataFrame,
    full_df: Optional[pd.DataFrame] = None,
    selected_year: Optional[int] = None,
) -> None:
    """
    Shows four readable country-level average KPI cards.

    These are simple averages across available country rows.
    They are not population-weighted global averages.
    """
    col1, col2, col3, col4 = st.columns(4)

    electricity_mean = safe_mean(year_df, "access_electricity")
    clean_fuel_mean = safe_mean(year_df, "access_clean_fuels")
    renewable_mean = safe_mean(year_df, "renewable_share")
    co2_mean = safe_mean(year_df, "co2_per_capita")

    selected_year_note = (
        f"Selected year: {selected_year}"
        if selected_year is not None
        else ""
    )

    co2_note = selected_year_note

    if co2_mean is None and full_df is not None and selected_year is not None:
        co2_mean, latest_year = latest_available_country_mean(
            full_df=full_df,
            column="co2_per_capita",
            selected_year=selected_year,
        )

        if latest_year is not None:
            co2_note = f"Latest available year: {latest_year}"
        else:
            co2_note = "No CO2 per-capita data available"

    with col1:
        kpi_card(
            title="Country avg. electricity access",
            value=format_number(
                electricity_mean,
                decimals=1,
                suffix="%",
            ),
            note=selected_year_note,
        )

    with col2:
        kpi_card(
            title="Country avg. clean fuel access",
            value=format_number(
                clean_fuel_mean,
                decimals=1,
                suffix="%",
            ),
            note=selected_year_note,
        )

    with col3:
        kpi_card(
            title="Country avg. renewable share",
            value=format_number(
                renewable_mean,
                decimals=1,
                suffix="%",
            ),
            note=selected_year_note,
        )

    with col4:
        kpi_card(
            title="Country avg. tCO2 per capita",
            value=f"{format_number(co2_mean, decimals=2)} tCO₂ per person",
            note=co2_note,
        )