# Global Sustainable Energy Dashboard

## Overview

This project is an interactive Streamlit dashboard for exploring global sustainable energy development across countries.

The dashboard compares countries using several sustainable energy and economic indicators, including:

- Access to electricity
- Access to clean fuels
- Renewable energy share
- Low-carbon electricity share
- Electricity generation mix
- GDP per capita
- CO₂ emissions per capita

The dashboard is designed to help users explore how the global transition toward sustainable energy differs between countries and changes over time.

## Main Dashboard Question

How has the global transition toward sustainable energy developed from 2000 to 2020, and how do countries differ in access, renewable adoption, electricity mix, and emissions?

## Key Analytical Questions

The dashboard helps answer the following questions:

1. Which countries have higher or lower access to electricity and clean fuels?
2. How have sustainable energy indicators changed over time?
3. How do selected countries compare in renewable energy share and low-carbon electricity?
4. What share of electricity generation comes from fossil fuels, nuclear power, and renewables?
5. Is there a visible relationship between GDP per capita and CO₂ emissions per person?
6. Which countries rank highest or lowest on selected sustainability indicators?

## Dashboard Features

The dashboard includes six main visualisations:

1. Choropleth map for geographic comparison
2. Country-level trend chart
3. Selected-country comparison line chart
4. 100% stacked electricity generation mix chart
5. GDP per capita vs CO₂ emissions scatter plot
6. Country ranking bar chart

It also includes:

- Summary KPI cards
- Country quick-pick groups
- Continent selector
- Metric selectors
- Independent “use all countries” checkboxes
- Reset filters button
- Light/dark theme toggle
- Filtered data table

## Interaction Design

The sidebar is divided into collapsible sections:

- Time
- Geography
- Metrics
- Options

Users can filter by selected year, trend range, country group, continent, metric type, and ranking size.

Preset country groups include:

- Top 5
- Favorites
- BRICS
- NATO
- G7

The continent selector allows users to quickly select countries from a specific continent. If a continent is selected, it overrides the country quick-pick group.

Some dashboard sections include independent “use all countries” checkboxes. These allow the overview cards, trend chart, and scatter plot to switch between selected countries and all countries without changing the rest of the dashboard.

## Data Notes

Several dashboard values are simple country-level averages. They are not population-weighted global averages. This means each country contributes equally to the average, regardless of population size.

Low-carbon electricity is interpreted as electricity generated from nuclear power and renewables.

The electricity generation mix chart is shown as a percentage share, not absolute TWh. This makes it easier to compare countries with very different total electricity production levels.

CO₂ emissions per capita means metric tons of CO₂ per person.

Some charts may use the latest available year when complete data is not available for the selected year.

## Files Included

- `app.py` — main Streamlit dashboard
- `config.py` — dashboard settings, labels, country groups, and column aliases
- `data_loader.py` — data loading, cleaning, and preparation
- `ui_components.py` — reusable interface components and theme styling
- `visuals.py` — Plotly chart functions
- `requirements.txt` — required Python packages
- `global-data-on-sustainable-energy.csv` — dataset

## Requirements

The project uses:

- Python
- Streamlit
- Pandas
- NumPy
- Plotly

The `requirements.txt` file should contain:

```text
streamlit
pandas
numpy
plotly