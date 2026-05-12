"""
This file contains all Plotly visualisation functions used in app.py.

The dashboard supports both light and dark theme modes. The layout stays the same;
only chart colours/backgrounds change.
"""

from __future__ import annotations

from typing import List, Tuple

import pandas as pd
import plotly.express as px

from config import (
    COLOUR_SCALE,
    ELECTRICITY_MIX_LABELS,
    METRIC_LABELS,
)


# --------------------------------------------------
# Theme helpers
# --------------------------------------------------

def get_chart_theme(theme_mode: str = "Light") -> dict:
    """
    The layout stays the same.
    Only colours change.
    """
    if theme_mode == "Dark":
        return {
            "template": "plotly_dark",
            "paper_bg": "#111827",
            "plot_bg": "#111827",
            "text": "#F9FAFB",
            "grid": "#374151",
            "axis": "#D1D5DB",
            "legend_bg": "#111827",
            
            
        }

    return {
       "template": "plotly_white",
        "paper_bg": "#FFFFFF",
        "plot_bg": "#FFFFFF",
        "text": "#111827",
        "grid": "#E5E7EB",
        "axis": "#374151",
        "legend_bg": "#FFFFFF",
    }


def apply_standard_layout(
    fig,
    height: int = 500,
    theme_mode: str = "Light",
):
    """
    Applies consistent styling to Plotly charts.

    This gives all charts a consistent professional appearance.
    """
    theme = get_chart_theme(theme_mode)

    fig.update_layout(
        template=theme["template"],
        height=height,
        margin=dict(l=35, r=35, t=70, b=55),
        legend_title_text="",
        font=dict(
            size=13,
            color=theme["text"],
            family="Arial, sans-serif",
        ),
        paper_bgcolor=theme["paper_bg"],
        plot_bgcolor=theme["plot_bg"],
        hoverlabel=dict(
            font_size=13,
            bgcolor=theme["paper_bg"],
            font_color=theme["text"],
            bordercolor=theme["grid"],
        ),
        legend=dict(
            bgcolor=theme["legend_bg"],
            font=dict(color=theme["text"]),
        ),
    )

    fig.update_xaxes(
        showgrid=True,
        gridcolor=theme["grid"],
        zeroline=False,
        linecolor=theme["grid"],
        tickfont=dict(color=theme["axis"]),
        title_font=dict(color=theme["text"]),
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor=theme["grid"],
        zeroline=False,
        linecolor=theme["grid"],
        tickfont=dict(color=theme["axis"]),
        title_font=dict(color=theme["text"]),
    )

    return fig


# --------------------------------------------------
# Visualisation 1 - Choropleth map
# --------------------------------------------------

def create_choropleth_map(
    map_df: pd.DataFrame,
    metric: str,
    selected_year: int,
    theme_mode: str = "Light",
):
    """
    Visualisation 1:
    Creates a choropleth map for a selected metric and year.

    Purpose:
    Shows geographic differences between countries.
    """
    theme = get_chart_theme(theme_mode)

    fig = px.choropleth(
        map_df,
        locations="country",
        locationmode="country names",
        color=metric,
        hover_name="country",
        hover_data={
            "year": True,
            metric: ":.2f",
        },
        color_continuous_scale=COLOUR_SCALE,
        title=f"{METRIC_LABELS.get(metric, metric)} by Country in {selected_year}",
    )

    fig.update_geos(
        showframe=False,
        showcoastlines=True,
        projection_type="natural earth",
        bgcolor=theme["paper_bg"],
    )

    fig.update_layout(
        template=theme["template"],
        height=500,
        margin=dict(l=0, r=0, t=65, b=0),
        paper_bgcolor=theme["paper_bg"],
        plot_bgcolor=theme["plot_bg"],
        font=dict(
            size=13,
            color=theme["text"],
            family="Arial, sans-serif",
        ),
        coloraxis_colorbar=dict(
            title=METRIC_LABELS.get(metric, metric),
            tickfont=dict(color=theme["axis"]),
        ),
    )

    fig.update_coloraxes(
        colorbar_title_font=dict(
            color=theme["text"],
        )
    )

    return fig


# --------------------------------------------------
# Visualisation 2 - Global / selected-country trend
# --------------------------------------------------

def create_global_trend(
    trend_df: pd.DataFrame,
    metric: str,
    selected_year_range: Tuple[int, int],
    theme_mode: str = "Light",
):
    """
    Visualisation 2:
    Creates a line chart showing one selected country-level average metric over time.

    Each point is the simple average across the countries included in the section.
    """
    global_trend = (
        trend_df
        .dropna(subset=[metric])
        .groupby("year", as_index=False)
        .agg(
            average_value=(metric, "mean"),
            countries_included=("country", "nunique"),
        )
    )

    fig = px.line(
        global_trend,
        x="year",
        y="average_value",
        markers=True,
        title=(
            f"Country-Level Average: {METRIC_LABELS.get(metric, metric)}, "
            f"{selected_year_range[0]}–{selected_year_range[1]}"
        ),
        labels={
            "year": "Year",
            "average_value": f"Average country value: {METRIC_LABELS.get(metric, metric)}",
            "countries_included": "Countries included",
        },
        hover_data={
            "average_value": ":.2f",
            "countries_included": True,
        },
    )

    return apply_standard_layout(
        fig,
        height=500,
        theme_mode=theme_mode,
    )


# --------------------------------------------------
# Visualisation 3 - Selected country trend
# --------------------------------------------------

def create_country_trend(
    country_trend_df: pd.DataFrame,
    metric: str,
    theme_mode: str = "Light",
):
    """
    Visualisation 3:
    Creates a country comparison line chart for a selected metric.

    Purpose:
    Allows users to compare selected countries over time.
    """
    fig = px.line(
        country_trend_df,
        x="year",
        y=metric,
        color="country",
        markers=True,
        title=f"{METRIC_LABELS.get(metric, metric)} for Selected Countries",
        labels={
            "year": "Year",
            metric: METRIC_LABELS.get(metric, metric),
            "country": "Country",
        },
        hover_data={
            "country": True,
            "year": True,
            metric: ":.2f",
        },
    )

    return apply_standard_layout(
        fig,
        height=500,
        theme_mode=theme_mode,
    )


# --------------------------------------------------
# Visualisation 4 - Electricity generation mix
# --------------------------------------------------

def create_electricity_mix_chart(
    mix_df: pd.DataFrame,
    electricity_mix_columns: List[str],
    selected_year: int,
    theme_mode: str = "Light",
):
    """
    Visualisation 4:
    Creates a 100% stacked bar chart showing electricity generation mix.

    Purpose:
    Shows what share of each selected country's electricity comes from
    fossil fuels, nuclear power, and renewables.

    This is better than absolute TWh when comparing reliance/mix,
    because large countries otherwise dominate the chart.
    """
    mix_long = mix_df.melt(
        id_vars=["country", "year"],
        value_vars=electricity_mix_columns,
        var_name="source",
        value_name="electricity_twh",
    )

    mix_long["source_label"] = mix_long["source"].map(ELECTRICITY_MIX_LABELS)

    mix_long = mix_long.dropna(
        subset=["electricity_twh"]
    ).copy()

    total_by_country = (
        mix_long
        .groupby("country", as_index=False)["electricity_twh"]
        .sum()
        .rename(columns={"electricity_twh": "total_electricity_twh"})
    )

    mix_long = mix_long.merge(
        total_by_country,
        on="country",
        how="left",
    )

    mix_long = mix_long[
        mix_long["total_electricity_twh"] > 0
    ].copy()

    mix_long["share_percent"] = (
        mix_long["electricity_twh"]
        / mix_long["total_electricity_twh"]
        * 100
    )

    fig = px.bar(
        mix_long,
        x="country",
        y="share_percent",
        color="source_label",
        title=f"Electricity Generation Mix Share for Selected Countries in {selected_year}",
        labels={
            "country": "Country",
            "share_percent": "Share of electricity generation (%)",
            "source_label": "Source",
            "electricity_twh": "Electricity generation (TWh)",
            "total_electricity_twh": "Total electricity generation (TWh)",
        },
        hover_data={
            "share_percent": ":.1f",
            "electricity_twh": ":,.1f",
            "total_electricity_twh": ":,.1f",
        },
    )

    fig.update_layout(
        barmode="stack",
    )

    fig.update_yaxes(
        range=[0, 100],
        ticksuffix="%",
    )

    return apply_standard_layout(
        fig,
        height=520,
        theme_mode=theme_mode,
    )


# --------------------------------------------------
# Visualisation 5 - GDP vs CO2 scatter plot
# --------------------------------------------------

def create_gdp_co2_scatter(
    scatter_df: pd.DataFrame,
    selected_year: int,
    use_log_gdp_axis: bool,
    theme_mode: str = "Light",
):
    """
    Visualisation 5:
    Creates a scatter plot showing the relationship between GDP per capita
    and CO2 emissions per capita.

    Purpose:
    Explores whether wealthier countries tend to have higher emissions per person.
    """
    scatter_arguments = {
        "data_frame": scatter_df,
        "x": "gdp_per_capita",
        "y": "co2_per_capita",
        "hover_name": "country",
        "title": f"GDP per Capita vs CO₂ Emissions per Capita in {selected_year}",
        "labels": {
            "gdp_per_capita": "GDP per capita",
            "co2_per_capita": "CO₂ emissions per capita",
            "renewable_share": "Renewable energy share (%)",
            "estimated_population": "Estimated population",
        },
        "log_x": use_log_gdp_axis,
    }

    if (
        "renewable_share" in scatter_df.columns
        and scatter_df["renewable_share"].notna().any()
    ):
        scatter_arguments["color"] = "renewable_share"
        scatter_arguments["color_continuous_scale"] = COLOUR_SCALE

    if (
        "estimated_population" in scatter_df.columns
        and scatter_df["estimated_population"].notna().any()
    ):
        size_df = scatter_df[
            scatter_df["estimated_population"] > 0
        ].copy()

        if not size_df.empty:
            scatter_arguments["data_frame"] = size_df
            scatter_arguments["size"] = "estimated_population"
            scatter_arguments["size_max"] = 38

    fig = px.scatter(
        **scatter_arguments
    )

    return apply_standard_layout(
        fig,
        height=540,
        theme_mode=theme_mode,
    )


# --------------------------------------------------
# Visualisation 6 - Country ranking
# --------------------------------------------------

def create_country_ranking(
    ranking_df: pd.DataFrame,
    metric: str,
    top_n: int,
    selected_year: int,
    theme_mode: str = "Light",
):
    """
    Visualisation 6:
    Creates a horizontal bar chart ranking countries by a selected metric.

    For CO2 per capita, lower values are ranked first because lower emissions
    are more desirable from a sustainability perspective.

    GDP per capita values are formatted as compact currency labels,
    for example $65.3k instead of 65279.5.
    """
    ascending = metric == "co2_per_capita"

    ranking_df = ranking_df.sort_values(
        metric,
        ascending=ascending,
    ).head(top_n).copy()

    chart_title_prefix = "Lowest" if ascending else "Highest"

    # --------------------------------------------------
    # Format value labels
    # --------------------------------------------------

    if metric == "gdp_per_capita":
        ranking_df["label_text"] = ranking_df[metric].apply(
            lambda value: f"${value / 1000:.1f}k"
        )

    elif metric in [
        "access_electricity",
        "access_clean_fuels",
        "renewable_share",
        "low_carbon_electricity_pct",
    ]:
        ranking_df["label_text"] = ranking_df[metric].apply(
            lambda value: f"{value:.1f}%"
        )

    elif metric == "co2_per_capita":
        ranking_df["label_text"] = ranking_df[metric].apply(
            lambda value: f"{value:.2f} tCO₂"
        )

    else:
        ranking_df["label_text"] = ranking_df[metric].apply(
            lambda value: f"{value:,.1f}"
        )

    # --------------------------------------------------
    # Create chart
    # --------------------------------------------------

    fig = px.bar(
        ranking_df.sort_values(metric, ascending=True),
        x=metric,
        y="country",
        orientation="h",
        text="label_text",
        title=(
            f"{chart_title_prefix} {top_n} Countries by "
            f"{METRIC_LABELS.get(metric, metric)} in {selected_year}"
        ),
        labels={
            "country": "Country",
            metric: METRIC_LABELS.get(metric, metric),
        },
        hover_data={
            "country": True,
            metric: ":,.2f",
            "label_text": False,
        },
    )

    fig.update_traces(
        texttemplate="%{text}",
        textposition="outside",
        cliponaxis=False,
    )

    max_value = ranking_df[metric].max()

    if pd.notna(max_value) and max_value > 0:
        fig.update_xaxes(
            range=[0, max_value * 1.22],
        )

    if metric == "gdp_per_capita":
        fig.update_xaxes(
            tickprefix="$",
            tickformat=".3s",
            title_text="GDP per capita",
        )

    elif metric in [
        "access_electricity",
        "access_clean_fuels",
        "renewable_share",
        "low_carbon_electricity_pct",
    ]:
        fig.update_xaxes(
            ticksuffix="%",
        )

    fig = apply_standard_layout(
        fig,
        height=540,
        theme_mode=theme_mode,
    )

    fig.update_layout(
        margin=dict(
            l=35,
            r=140,
            t=70,
            b=55,
        )
    )

    return fig