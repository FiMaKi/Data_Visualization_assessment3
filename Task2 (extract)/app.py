"""
app.py

Main file for the Task 2 Streamlit dashboard.

Run with:
python3 -m streamlit run app.py
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

from config import (
    APP_SUBTITLE,
    APP_TITLE,
    ELECTRICITY_MIX_LABELS,
    METRIC_LABELS,
)

from data_loader import (
    load_and_clean_data,
    remove_aggregate_entities,
)

from helpers import (
    get_latest_available_year_for_columns,
)

from sidebar import (
    build_sidebar,
    initialise_theme,
)

from ui_components import (
    inject_custom_css,
    section_header,
    show_kpi_cards,
)

from visuals import (
    create_choropleth_map,
    create_country_ranking,
    create_country_trend,
    create_electricity_mix_chart,
    create_gdp_co2_scatter,
    create_global_trend,
)


# --------------------------------------------------
# 1. Page setup
# --------------------------------------------------

st.set_page_config(
    page_title="Global Sustainable Energy Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

theme_mode = initialise_theme()

inject_custom_css(theme_mode)


# --------------------------------------------------
# 2. Load and prepare data
# --------------------------------------------------

try:
    df, matched_columns, missing_columns, data_path = load_and_clean_data()

except Exception as error:
    st.error("The dashboard could not load the dataset.")
    st.exception(error)
    st.stop()


country_df = remove_aggregate_entities(df)

if country_df.empty:
    st.error(
        "No country-level data is available after cleaning. "
        "Check whether the dataset contains country rows."
    )
    st.stop()


# --------------------------------------------------
# 3. Sidebar filters
# --------------------------------------------------
# The full sidebar is now handled in sidebar.py.
# This keeps app.py focused on dashboard layout and visualisation flow.

sidebar_values = build_sidebar(country_df)

min_year = sidebar_values["min_year"]
max_year = sidebar_values["max_year"]

selected_year = sidebar_values["selected_year"]
selected_year_range = sidebar_values["selected_year_range"]

selected_country_group = sidebar_values["selected_country_group"]
selected_continent = sidebar_values["selected_continent"]
selected_countries = sidebar_values["selected_countries"]

selected_map_metric = sidebar_values["selected_map_metric"]
selected_global_trend_metric = sidebar_values["selected_global_trend_metric"]
selected_country_trend_metric = sidebar_values["selected_country_trend_metric"]
selected_ranking_metric = sidebar_values["selected_ranking_metric"]

top_n = sidebar_values["top_n"]
use_log_gdp_axis = sidebar_values["use_log_gdp_axis"]
show_cleaning_details = sidebar_values["show_cleaning_details"]


# --------------------------------------------------
# 4. Dashboard header
# --------------------------------------------------

with st.container(border=True):
    st.markdown(f"### 🌍 {APP_TITLE}")

    st.caption(APP_SUBTITLE)

    header_col1, header_col2, header_col3 = st.columns(3)

    with header_col1:
        st.caption("Selected year")
        st.markdown(f"**{selected_year}**")

    with header_col2:
        st.caption("Trend period")
        st.markdown(f"**{selected_year_range[0]}–{selected_year_range[1]}**")

    with header_col3:
        st.caption("Countries selected")
        st.markdown(f"**{len(selected_countries)}**")


# --------------------------------------------------
# 5. Optional data checks
# --------------------------------------------------

if show_cleaning_details:
    with st.expander("Data checks and matched columns", expanded=True):
        st.write("### Matched dataset columns")

        matched_table = pd.DataFrame(
            [
                {
                    "Internal name used in code": internal,
                    "Original column in CSV": original,
                }
                for internal, original in matched_columns.items()
            ]
        )

        st.dataframe(
            matched_table,
            use_container_width=True,
            hide_index=True,
        )

        st.write("### Missing optional columns")

        missing_optional_table = pd.DataFrame(
            {
                "Missing internal column": missing_columns
            }
        )

        st.dataframe(
            missing_optional_table,
            use_container_width=True,
            hide_index=True,
        )

        st.write("### Dataset size")

        dataset_size_table = pd.DataFrame(
            [
                {
                    "Description": "Rows after initial cleaning",
                    "Value": len(df),
                },
                {
                    "Description": "Country-level rows after removing aggregate entities",
                    "Value": len(country_df),
                },
                {
                    "Description": "Minimum year in dataset",
                    "Value": min_year,
                },
                {
                    "Description": "Maximum year in dataset",
                    "Value": max_year,
                },
            ]
        )

        st.dataframe(
            dataset_size_table,
            use_container_width=True,
            hide_index=True,
        )

        st.write("### Current sidebar selection")

        current_selection_table = pd.DataFrame(
            [
                {
                    "Setting": "Selected year",
                    "Value": selected_year,
                },
                {
                    "Setting": "Trend year range",
                    "Value": f"{selected_year_range[0]}–{selected_year_range[1]}",
                },
                {
                    "Setting": "Country quick pick",
                    "Value": selected_country_group,
                },
                {
                    "Setting": "Continent selector",
                    "Value": selected_continent,
                },
                {
                    "Setting": "Number of selected countries",
                    "Value": len(selected_countries),
                },
                {
                    "Setting": "Selected countries",
                    "Value": ", ".join(selected_countries) if selected_countries else "None",
                },
                {
                    "Setting": "Map metric",
                    "Value": METRIC_LABELS.get(selected_map_metric, selected_map_metric),
                },
                {
                    "Setting": "Global trend metric",
                    "Value": METRIC_LABELS.get(
                        selected_global_trend_metric,
                        selected_global_trend_metric,
                    ),
                },
                {
                    "Setting": "Country trend metric",
                    "Value": METRIC_LABELS.get(
                        selected_country_trend_metric,
                        selected_country_trend_metric,
                    ),
                },
                {
                    "Setting": "Ranking metric",
                    "Value": METRIC_LABELS.get(
                        selected_ranking_metric,
                        selected_ranking_metric,
                    ),
                },
            ]
        )

        st.dataframe(
            current_selection_table,
            use_container_width=True,
            hide_index=True,
        )


# --------------------------------------------------
# 6. Filter data according to sidebar choices
# --------------------------------------------------

year_df = country_df[
    country_df["year"] == selected_year
].copy()

trend_df = country_df[
    (country_df["year"] >= selected_year_range[0])
    & (country_df["year"] <= selected_year_range[1])
].copy()

if selected_countries:
    selected_country_df = trend_df[
        trend_df["country"].isin(selected_countries)
    ].copy()

else:
    selected_country_df = pd.DataFrame(
        columns=trend_df.columns
    )


selected_year_country_count = year_df["country"].nunique()
selected_trend_country_count = trend_df["country"].nunique()
selected_country_data_count = selected_country_df["country"].nunique()

st.caption(
    f"Selected year data includes {selected_year_country_count} countries. "
    f"The trend range {selected_year_range[0]}–{selected_year_range[1]} includes "
    f"{selected_trend_country_count} countries. "
    f"Current comparison selection includes {selected_country_data_count} countries with data."
)


# --------------------------------------------------
# 7. KPI cards
# --------------------------------------------------

section_header(
    "Overview for Selected Year",
    (
        "These summary cards show simple country-level averages for the selected year. "
        "By default, they use the countries selected in the sidebar."
    ),
)

overview_use_all_countries = st.checkbox(
    "Use all countries for overview cards",
    value=False,
    key="overview_use_all_countries",
)

if overview_use_all_countries:
    overview_year_df = year_df.copy()
    overview_full_df = country_df.copy()
    overview_source_label = "all countries"

else:
    overview_year_df = year_df[
        year_df["country"].isin(selected_countries)
    ].copy()

    overview_full_df = country_df[
        country_df["country"].isin(selected_countries)
    ].copy()

    overview_source_label = "selected countries"


if overview_year_df.empty:
    st.warning(
        "No overview data is available for the current country selection and selected year."
    )

else:
    st.caption(
        f"Overview cards are currently calculated using {overview_source_label} "
        f"for {selected_year}. These are simple country-level averages, not population-weighted averages."
    )

    show_kpi_cards(
        year_df=overview_year_df,
        full_df=overview_full_df,
        selected_year=selected_year,
    )


# --------------------------------------------------
# 8. Visualisation 1 - Choropleth map
# --------------------------------------------------

section_header(
    "1. Geographic Distribution",
    "This map shows how the selected sustainability indicator differs between countries.",
)

map_df = year_df.dropna(
    subset=[selected_map_metric]
).copy()

if map_df.empty:
    st.warning("No data is available for the selected map metric and year.")

else:
    fig_map = create_choropleth_map(
        map_df=map_df,
        metric=selected_map_metric,
        selected_year=selected_year,
        theme_mode=theme_mode,
    )

    st.plotly_chart(
        fig_map,
        use_container_width=True,
    )

# --------------------------------------------------
# 9. Visualisation 2 - Country-level trend
# --------------------------------------------------

global_trend_use_all_countries = st.checkbox(
    "Use all countries for this trend",
    value=False,
    key="global_trend_use_all_countries",
)

if global_trend_use_all_countries:
    global_trend_source_df = trend_df.copy()
    global_trend_source_label = "all countries"
    global_trend_section_title = "2. Global Country-Level Trend"
    global_trend_section_note = (
        "This line chart shows the selected indicator over time using all countries "
        "with available data."
    )

else:
    global_trend_source_df = trend_df[
        trend_df["country"].isin(selected_countries)
    ].copy()

    global_trend_source_label = "selected countries"
    global_trend_section_title = "2. Selected Countries Trend"
    global_trend_section_note = (
        "This line chart shows the selected indicator over time using only the "
        "countries selected in the sidebar."
    )


section_header(
    global_trend_section_title,
    global_trend_section_note,
)

if selected_global_trend_metric not in global_trend_source_df.columns:
    st.warning("No suitable trend metric is available.")

else:
    global_trend_df = global_trend_source_df.dropna(
        subset=[selected_global_trend_metric]
    ).copy()

    if global_trend_df.empty:
        st.warning(
            "No data is available for the selected trend metric and country selection."
        )

    else:
        countries_in_global_trend = global_trend_df["country"].nunique()

        st.caption(
            f"This trend uses {global_trend_source_label}: "
            f"{countries_in_global_trend} countries with available data for "
            f"{METRIC_LABELS.get(selected_global_trend_metric, selected_global_trend_metric)}."
        )

        fig_global_trend = create_global_trend(
            trend_df=global_trend_df,
            metric=selected_global_trend_metric,
            selected_year_range=selected_year_range,
            theme_mode=theme_mode,
        )

        st.plotly_chart(
            fig_global_trend,
            use_container_width=True,
        )


# --------------------------------------------------
# 10. Visualisation 3 - Selected country trend
# --------------------------------------------------

section_header(
    "3. Country Comparison Over Time",
    (
        "This chart compares the selected countries across the chosen time period. "
        "The countries shown come from the sidebar quick pick, continent selector, "
        "or manual country selection."
    ),
)

if not selected_countries:
    st.warning(
        "No countries are currently selected. Choose countries in the sidebar to show this chart."
    )

else:
    country_trend_df = selected_country_df.dropna(
        subset=[selected_country_trend_metric]
    ).copy()

    if country_trend_df.empty:
        st.warning(
            "No data is available for the selected countries and the selected trend metric."
        )

    else:
        countries_with_data = sorted(
            country_trend_df["country"].dropna().unique()
        )

        countries_without_data = [
            country for country in selected_countries
            if country not in countries_with_data
        ]

        st.caption(
            f"Showing {len(countries_with_data)} countries with available data "
            f"for {METRIC_LABELS.get(selected_country_trend_metric, selected_country_trend_metric)}."
        )

        if len(countries_with_data) > 12:
            st.info(
                "Many countries are selected, so the line chart may look crowded. "
                "For clearer comparison, use a smaller quick-pick group or manually reduce the country list."
            )

        if countries_without_data:
            st.caption(
                "Selected countries without data for this metric: "
                + ", ".join(countries_without_data)
            )

        fig_country_trend = create_country_trend(
            country_trend_df=country_trend_df,
            metric=selected_country_trend_metric,
            theme_mode=theme_mode,
        )

        st.plotly_chart(
            fig_country_trend,
            use_container_width=True,
        )


# --------------------------------------------------
# 11. Visualisation 4 - Electricity generation mix
# --------------------------------------------------

section_header(
    "4. Electricity Generation Mix",
    (
        "This 100% stacked bar chart shows the share of electricity generated from "
        "fossil fuels, nuclear power, and renewables for the selected countries."
    ),
)

electricity_mix_columns = [
    column for column in ELECTRICITY_MIX_LABELS.keys()
    if column in year_df.columns
]

if len(electricity_mix_columns) < 2:
    st.warning(
        "Electricity mix chart needs at least two electricity generation columns, "
        "such as fossil fuels, nuclear, and renewables."
    )

else:
    mix_df = year_df[
        year_df["country"].isin(selected_countries)
    ].copy()

    if mix_df.empty:
        st.warning(
            "Select countries in the sidebar to show the electricity mix chart."
        )

    else:
        countries_in_mix = mix_df["country"].nunique()

        st.caption(
            f"Showing electricity generation shares for {countries_in_mix} selected countries "
            f"in {selected_year}."
        )

        fig_mix = create_electricity_mix_chart(
            mix_df=mix_df,
            electricity_mix_columns=electricity_mix_columns,
            selected_year=selected_year,
            theme_mode=theme_mode,
        )

        st.plotly_chart(
            fig_mix,
            use_container_width=True,
        )


# --------------------------------------------------
# 12. Visualisation 5 - GDP vs CO2 scatter plot
# --------------------------------------------------

section_header(
    "5. Economic Context and Emissions",
    (
        "This scatter plot explores whether countries with higher GDP per capita "
        "also tend to have higher CO2 emissions per person."
    ),
)

scatter_use_all_countries = st.checkbox(
    "Use all countries for this scatter plot",
    value=False,
    key="scatter_use_all_countries",
)

required_scatter_columns = [
    "gdp_per_capita",
    "co2_per_capita",
]

if scatter_use_all_countries:
    scatter_base_df = country_df.copy()
    scatter_year_df = year_df.copy()
    scatter_source_label = "all countries"

else:
    scatter_base_df = country_df[
        country_df["country"].isin(selected_countries)
    ].copy()

    scatter_year_df = year_df[
        year_df["country"].isin(selected_countries)
    ].copy()

    scatter_source_label = "selected countries"


if not all(column in scatter_base_df.columns for column in required_scatter_columns):
    st.warning(
        "The scatter plot needs GDP per capita and CO2 emissions per capita. "
        "One or both of these columns are missing from the cleaned dataset."
    )

else:
    scatter_year_used = selected_year

    scatter_df = scatter_year_df.dropna(
        subset=required_scatter_columns
    ).copy()

    if use_log_gdp_axis:
        scatter_df = scatter_df[
            scatter_df["gdp_per_capita"] > 0
        ].copy()

    if scatter_df.empty:
        fallback_year = get_latest_available_year_for_columns(
            df=scatter_base_df,
            columns=required_scatter_columns,
            selected_year=selected_year,
        )

        if fallback_year is not None:
            scatter_year_used = fallback_year

            scatter_df = scatter_base_df[
                scatter_base_df["year"] == fallback_year
            ].dropna(
                subset=required_scatter_columns
            ).copy()

            if use_log_gdp_axis:
                scatter_df = scatter_df[
                    scatter_df["gdp_per_capita"] > 0
                ].copy()

    if scatter_df.empty:
        st.warning(
            "No data is available for GDP per capita and CO2 emissions per capita "
            "for this country selection. Try selecting all countries or choosing another year."
        )

    else:
        st.caption(
            f"This scatter plot uses {scatter_source_label}: "
            f"{len(scatter_df)} countries with complete GDP and CO2 data "
            f"for {scatter_year_used}."
        )

        fig_scatter = create_gdp_co2_scatter(
            scatter_df=scatter_df,
            selected_year=scatter_year_used,
            use_log_gdp_axis=use_log_gdp_axis,
            theme_mode=theme_mode,
        )

        st.plotly_chart(
            fig_scatter,
            use_container_width=True,
        )

        if scatter_year_used != selected_year:
            st.caption(
                f"The selected year, {selected_year}, had no complete GDP and CO2 data "
                f"for this country selection. This chart therefore uses the latest "
                f"available year: {scatter_year_used}."
            )


# --------------------------------------------------
# 13. Visualisation 6 - Country ranking
# --------------------------------------------------

section_header(
    "6. Country Ranking",
    (
        "This chart ranks countries by the selected sustainability indicator. "
        "Use the sidebar ranking metric to change what is being compared."
    ),
)

ranking_df = year_df.dropna(
    subset=[selected_ranking_metric]
).copy()

if ranking_df.empty:
    st.warning(
        "No data is available for the selected ranking metric and selected year."
    )

else:
    countries_available_for_ranking = ranking_df["country"].nunique()

    st.caption(
        f"Ranking uses {countries_available_for_ranking} countries with available data "
        f"for {METRIC_LABELS.get(selected_ranking_metric, selected_ranking_metric)} in {selected_year}."
    )

    fig_ranking = create_country_ranking(
        ranking_df=ranking_df,
        metric=selected_ranking_metric,
        top_n=top_n,
        selected_year=selected_year,
        theme_mode=theme_mode,
    )

    st.plotly_chart(
        fig_ranking,
        use_container_width=True,
    )

    if selected_ranking_metric == "co2_per_capita":
        st.caption(
            "For CO2 emissions per capita, lower values are ranked first because "
            "lower emissions are more desirable from a sustainability perspective."
        )


# --------------------------------------------------
# 14. Filtered data table
# --------------------------------------------------

with st.expander("View filtered data table"):
    table_columns = [
        "country",
        "year",
        "access_electricity",
        "access_clean_fuels",
        "renewable_share",
        "low_carbon_electricity_pct",
        "co2_per_capita",
        "gdp_per_capita",
    ]

    table_columns = [
        column for column in table_columns
        if column in country_df.columns
    ]

    st.dataframe(
        year_df[table_columns].sort_values("country"),
        use_container_width=True,
        hide_index=True,
    )

    csv_data = year_df[table_columns].to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download selected-year data as CSV",
        data=csv_data,
        file_name=f"sustainable_energy_{selected_year}_filtered.csv",
        mime="text/csv",
    )


# --------------------------------------------------
# 15. Footer
# --------------------------------------------------

st.markdown("---")

st.caption(
    "Values are based on available country-level records in the sustainable energy dataset. "
    "Some averages are simple country-level averages and should not be interpreted as "
    "population-weighted global estimates unless explicitly stated."
)