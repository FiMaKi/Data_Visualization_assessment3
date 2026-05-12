"""
config.py

Project-wide settings for the Task 2 sustainable energy dashboard.

This file contains:
- dashboard titles and text
- dataset file locations
- aggregate entities to remove
- column aliases
- country quick-pick groups
- continent groups
- metric labels
- default dashboard settings
- chart style settings
"""

from pathlib import Path


# --------------------------------------------------
# Dashboard text
# --------------------------------------------------

APP_TITLE = "Global Sustainable Energy Dashboard"

APP_SUBTITLE = (
    "Compare countries by energy access, renewable adoption, electricity mix, "
    "GDP, and CO2 emissions."
)

DASHBOARD_QUESTION = (
    "How has the global transition toward sustainable energy developed from 2000 to 2020, "
    "and how do countries differ in access, renewable adoption, electricity mix, and emissions?"
)


# --------------------------------------------------
# File locations
# --------------------------------------------------
# This makes the project portable because it looks in the same folder as config.py/app.py.
# This is better for submission and deployment than using a Mac-specific file path.

LOCAL_TASK2_FOLDER = Path(__file__).resolve().parent

DATA_FILE_CANDIDATES = [
    "global-data-on-sustainable-energy.csv",
    "Global-data-on-sustainable-energy.csv",
    "global_data_on_sustainable_energy.csv",
    "global data on sustainable energy.csv",
]


# --------------------------------------------------
# Aggregate entities to remove
# --------------------------------------------------
# These are regions, income groups, or aggregate categories rather than individual countries.

AGGREGATE_ENTITIES = {
    "World",
    "Africa",
    "Asia",
    "Europe",
    "European Union",
    "North America",
    "South America",
    "Oceania",
    "High income",
    "Low income",
    "Lower middle income",
    "Upper middle income",
    "Arab World",
    "Central Europe and the Baltics",
    "Early-demographic dividend",
    "East Asia & Pacific",
    "East Asia & Pacific (IDA & IBRD)",
    "East Asia & Pacific (excluding high income)",
    "Euro area",
    "Europe & Central Asia",
    "Europe & Central Asia (IDA & IBRD)",
    "Europe & Central Asia (excluding high income)",
    "Fragile and conflict affected situations",
    "Heavily indebted poor countries (HIPC)",
    "IBRD only",
    "IDA & IBRD total",
    "IDA blend",
    "IDA only",
    "IDA total",
    "Late-demographic dividend",
    "Latin America & Caribbean",
    "Latin America & Caribbean (IDA & IBRD)",
    "Latin America & Caribbean (excluding high income)",
    "Least developed countries: UN classification",
    "Low & middle income",
    "Middle East & North Africa",
    "Middle East & North Africa (IDA & IBRD)",
    "Middle East & North Africa (excluding high income)",
    "Middle income",
    "OECD members",
    "Other small states",
    "Pacific island small states",
    "Post-demographic dividend",
    "Pre-demographic dividend",
    "Small states",
    "South Asia",
    "South Asia (IDA & IBRD)",
    "Sub-Saharan Africa",
    "Sub-Saharan Africa (IDA & IBRD)",
    "Sub-Saharan Africa (excluding high income)",
}


# --------------------------------------------------
# Column aliases
# --------------------------------------------------
# The same dataset can sometimes have slightly different column names.
# These aliases make the code more reliable.

COLUMN_ALIASES = {
    "country": [
        "Entity",
        "Country",
        "Country Name",
    ],

    "year": [
        "Year",
    ],

    "access_electricity": [
        "Access to electricity (%)",
        "Access to electricity",
        "Access to electricity (% of population)",
        "access_to_electricity",
    ],

    "access_clean_fuels": [
        "Access to clean fuels (%)",
        "Access to clean fuels",
        "Access to clean fuels for cooking",
        "Access to clean fuels and technologies for cooking (%)",
        "Access to clean fuels and technologies for cooking (% of population)",
        "access_to_clean_fuels",
    ],

    "renewable_capacity_per_capita": [
        "Renewable electricity capacity per capita",
        "Renewable-electricity-generating-capacity-per-capita",
        "Renewable electricity generating capacity per capita",
    ],

    "financial_flows_usd": [
        "Financial flows (USD)",
        "Financial flows to developing countries (US $)",
        "Financial flows to developing countries",
    ],

    "renewable_share": [
        "Renewable energy share (%)",
        "Renewable energy share in the total final energy consumption (%)",
        "Renewable energy share in total final energy consumption (%)",
    ],

    "electricity_fossil_twh": [
        "Electricity from fossil fuels (TWh)",
    ],

    "electricity_nuclear_twh": [
        "Electricity from nuclear (TWh)",
    ],

    "electricity_renewables_twh": [
        "Electricity from renewables (TWh)",
    ],

    "low_carbon_electricity_pct": [
        "Low-carbon electricity (% electricity)",
        "Low carbon electricity (% electricity)",
    ],

    "primary_energy_per_capita": [
        "Primary energy consumption per capita (kWh/person)",
    ],

    "energy_intensity": [
        "Energy intensity level of primary energy (MJ/$2011 PPP GDP)",
        "Energy intensity level of primary energy (MJ/$2017 PPP GDP)",
        "Energy intensity level of primary energy",
    ],

    "co2_per_capita": [
        "Value co2 emissions (metric tons per capita)",
        "CO2 emissions per capita",
        "CO₂ emissions per capita",
    ],

    "co2_total_kt": [
        "Value_co2_emissions_kt_by_country",
        "Value co2 emissions kt by country",
        "CO2 emissions kt by country",
    ],

    "renewables_equivalent": [
        "Renewables",
        "Renewables (% equivalent primary energy)",
    ],

    "gdp_growth": [
        "GDP growth (%)",
        "gdp_growth",
    ],

    "gdp_per_capita": [
        "GDP per capita",
        "gdp_per_capita",
    ],

    "population_density": [
        "Population density (P/Km2)",
        "Population density (P/Km²)",
        "Density\\n(P/Km2)",
        "Density\n(P/Km2)",
        "Density (P/Km2)",
    ],

    "land_area": [
        "Land area (Km2)",
        "Land Area(Km2)",
        "Land Area (Km2)",
    ],

    "latitude": [
        "Latitude",
    ],

    "longitude": [
        "Longitude",
    ],
}


# --------------------------------------------------
# Default country selection
# --------------------------------------------------

DEFAULT_COUNTRIES = [
    "United States",
    "China",
    "Russia",
    "India",
    "United Kingdom",
]


# --------------------------------------------------
# Country quick-pick groups
# --------------------------------------------------
# These groups are used in the sidebar to quickly select meaningful country sets.

COUNTRY_GROUPS = {
    "Top 5": [
        "United States",
        "China",
        "Russia",
        "India",
        "United Kingdom",
    ],

    "Favorites": [
        "United States",
        "Norway",
        "China",
        "Russia",
        "Brazil",
        "Germany",
        "United Kingdom",
        "United Arab Emirates",
    ],

    "BRICS": [
        "Brazil",
        "Russia",
        "India",
        "China",
        "South Africa",
        "Egypt",
        "Ethiopia",
        "Iran",
        "Saudi Arabia",
        "United Arab Emirates",
        "Indonesia",
    ],

    "NATO": [
        "Albania",
        "Belgium",
        "Bulgaria",
        "Canada",
        "Croatia",
        "Czechia",
        "Denmark",
        "Estonia",
        "Finland",
        "France",
        "Germany",
        "Greece",
        "Hungary",
        "Iceland",
        "Italy",
        "Latvia",
        "Lithuania",
        "Luxembourg",
        "Montenegro",
        "Netherlands",
        "North Macedonia",
        "Norway",
        "Poland",
        "Portugal",
        "Romania",
        "Slovakia",
        "Slovenia",
        "Spain",
        "Sweden",
        "Turkey",
        "United Kingdom",
        "United States",
    ],

    "G7": [
        "Canada",
        "France",
        "Germany",
        "Italy",
        "Japan",
        "United Kingdom",
        "United States",
    ],
}


# --------------------------------------------------
# Country name aliases
# --------------------------------------------------
# This helps if the CSV uses slightly different country names.

COUNTRY_NAME_ALIASES = {
    "Russia": [
        "Russia",
        "Russian Federation",
    ],

    "United States": [
        "United States",
        "United States of America",
        "USA",
    ],

    "United Kingdom": [
        "United Kingdom",
        "United Kingdom of Great Britain and Northern Ireland",
        "UK",
    ],

    "United Arab Emirates": [
        "United Arab Emirates",
        "UAE",
    ],

    "Turkey": [
        "Turkey",
        "Türkiye",
        "Turkiye",
    ],

    "Czechia": [
        "Czechia",
        "Czech Republic",
    ],

    "Iran": [
        "Iran",
        "Iran, Islamic Republic of",
    ],

    "South Korea": [
        "South Korea",
        "Korea, Republic of",
    ],

    "North Korea": [
        "North Korea",
        "Korea, Democratic People's Republic of",
    ],

    "Democratic Republic of Congo": [
        "Democratic Republic of Congo",
        "Congo, Dem. Rep.",
        "Democratic Republic of the Congo",
    ],

    "Congo": [
        "Congo",
        "Congo, Rep.",
        "Republic of Congo",
    ],

    "Ivory Coast": [
        "Ivory Coast",
        "Cote d'Ivoire",
        "Côte d'Ivoire",
    ],

    "Laos": [
        "Laos",
        "Lao PDR",
    ],

    "Syria": [
        "Syria",
        "Syrian Arab Republic",
    ],

    "Venezuela": [
        "Venezuela",
        "Venezuela, RB",
    ],

    "Yemen": [
        "Yemen",
        "Yemen, Rep.",
    ],

    "Egypt": [
        "Egypt",
        "Egypt, Arab Rep.",
    ],
}


# --------------------------------------------------
# Continent quick-pick groups
# --------------------------------------------------
# Antarctica is included as an option, but it normally has no country-level rows
# in this dataset.

CONTINENT_GROUPS = {
    "None": [],

    "Africa": [
        "Algeria",
        "Angola",
        "Benin",
        "Botswana",
        "Burkina Faso",
        "Burundi",
        "Cameroon",
        "Cape Verde",
        "Central African Republic",
        "Chad",
        "Comoros",
        "Congo",
        "Democratic Republic of Congo",
        "Djibouti",
        "Egypt",
        "Equatorial Guinea",
        "Eritrea",
        "Eswatini",
        "Ethiopia",
        "Gabon",
        "Gambia",
        "Ghana",
        "Guinea",
        "Guinea-Bissau",
        "Ivory Coast",
        "Kenya",
        "Lesotho",
        "Liberia",
        "Libya",
        "Madagascar",
        "Malawi",
        "Mali",
        "Mauritania",
        "Mauritius",
        "Morocco",
        "Mozambique",
        "Namibia",
        "Niger",
        "Nigeria",
        "Rwanda",
        "Sao Tome and Principe",
        "Senegal",
        "Seychelles",
        "Sierra Leone",
        "Somalia",
        "South Africa",
        "South Sudan",
        "Sudan",
        "Tanzania",
        "Togo",
        "Tunisia",
        "Uganda",
        "Zambia",
        "Zimbabwe",
    ],

    "Antarctica": [],

    "Asia": [
        "Afghanistan",
        "Armenia",
        "Azerbaijan",
        "Bahrain",
        "Bangladesh",
        "Bhutan",
        "Brunei",
        "Cambodia",
        "China",
        "Cyprus",
        "Georgia",
        "India",
        "Indonesia",
        "Iran",
        "Iraq",
        "Israel",
        "Japan",
        "Jordan",
        "Kazakhstan",
        "Kuwait",
        "Kyrgyzstan",
        "Laos",
        "Lebanon",
        "Malaysia",
        "Maldives",
        "Mongolia",
        "Myanmar",
        "Nepal",
        "North Korea",
        "Oman",
        "Pakistan",
        "Palestine",
        "Philippines",
        "Qatar",
        "Saudi Arabia",
        "Singapore",
        "South Korea",
        "Sri Lanka",
        "Syria",
        "Tajikistan",
        "Thailand",
        "Timor-Leste",
        "Turkey",
        "Turkmenistan",
        "United Arab Emirates",
        "Uzbekistan",
        "Vietnam",
        "Yemen",
    ],

    "Europe": [
        "Albania",
        "Andorra",
        "Austria",
        "Belarus",
        "Belgium",
        "Bosnia and Herzegovina",
        "Bulgaria",
        "Croatia",
        "Czechia",
        "Denmark",
        "Estonia",
        "Finland",
        "France",
        "Germany",
        "Greece",
        "Hungary",
        "Iceland",
        "Ireland",
        "Italy",
        "Kosovo",
        "Latvia",
        "Liechtenstein",
        "Lithuania",
        "Luxembourg",
        "Malta",
        "Moldova",
        "Montenegro",
        "Netherlands",
        "North Macedonia",
        "Norway",
        "Poland",
        "Portugal",
        "Romania",
        "Russia",
        "San Marino",
        "Serbia",
        "Slovakia",
        "Slovenia",
        "Spain",
        "Sweden",
        "Switzerland",
        "Ukraine",
        "United Kingdom",
    ],

    "North America": [
        "Antigua and Barbuda",
        "Bahamas",
        "Barbados",
        "Belize",
        "Canada",
        "Costa Rica",
        "Cuba",
        "Dominica",
        "Dominican Republic",
        "El Salvador",
        "Grenada",
        "Guatemala",
        "Haiti",
        "Honduras",
        "Jamaica",
        "Mexico",
        "Nicaragua",
        "Panama",
        "Saint Kitts and Nevis",
        "Saint Lucia",
        "Saint Vincent and the Grenadines",
        "Trinidad and Tobago",
        "United States",
    ],

    "Oceania": [
        "Australia",
        "Fiji",
        "Kiribati",
        "Marshall Islands",
        "Micronesia",
        "Nauru",
        "New Zealand",
        "Palau",
        "Papua New Guinea",
        "Samoa",
        "Solomon Islands",
        "Tonga",
        "Tuvalu",
        "Vanuatu",
    ],

    "South America": [
        "Argentina",
        "Bolivia",
        "Brazil",
        "Chile",
        "Colombia",
        "Ecuador",
        "Guyana",
        "Paraguay",
        "Peru",
        "Suriname",
        "Uruguay",
        "Venezuela",
    ],
}


# --------------------------------------------------
# Dashboard metric labels
# --------------------------------------------------

METRIC_LABELS = {
    "access_electricity": "Access to electricity (%)",
    "access_clean_fuels": "Access to clean fuels (%)",
    "renewable_share": "Renewable energy share (%)",
    "low_carbon_electricity_pct": "Low-carbon electricity (% electricity)",
    "co2_per_capita": "CO2 emissions per capita",
    "gdp_per_capita": "GDP per capita",
    "primary_energy_per_capita": "Primary energy consumption per capita",
    "energy_intensity": "Energy intensity",
    "renewable_capacity_per_capita": "Renewable electricity capacity per capita",
    "financial_flows_usd": "Financial flows for clean energy (USD)",
}


ELECTRICITY_MIX_LABELS = {
    "electricity_fossil_twh": "Fossil fuels",
    "electricity_nuclear_twh": "Nuclear",
    "electricity_renewables_twh": "Renewables",
}


# --------------------------------------------------
# Dashboard metric options
# --------------------------------------------------

MAP_METRIC_OPTIONS = [
    "access_electricity",
    "access_clean_fuels",
    "renewable_share",
    "low_carbon_electricity_pct",
    "co2_per_capita",
    "gdp_per_capita",
    "primary_energy_per_capita",
]


GLOBAL_TREND_METRIC_OPTIONS = [
    "access_electricity",
    "access_clean_fuels",
    "renewable_share",
    "low_carbon_electricity_pct",
    "co2_per_capita",
    "primary_energy_per_capita",
]


COUNTRY_TREND_METRIC_OPTIONS = [
    "renewable_share",
    "low_carbon_electricity_pct",
    "access_electricity",
    "access_clean_fuels",
    "co2_per_capita",
    "primary_energy_per_capita",
]


RANKING_METRIC_OPTIONS = [
    "low_carbon_electricity_pct",
    "renewable_share",
    "access_electricity",
    "access_clean_fuels",
    "co2_per_capita",
    "gdp_per_capita",
]


# --------------------------------------------------
# Recommended default dashboard settings
# --------------------------------------------------
# These defaults make the app open with a strong, complete, sustainability-focused view.

DEFAULT_SELECTED_YEAR = 2019

DEFAULT_TREND_START_YEAR = 2000
DEFAULT_TREND_END_YEAR = 2019

DEFAULT_COUNTRY_GROUP = "Top 5"
DEFAULT_CONTINENT = "None"

DEFAULT_MAP_METRIC = "access_electricity"
DEFAULT_GLOBAL_TREND_METRIC = "access_electricity"
DEFAULT_COUNTRY_TREND_METRIC = "renewable_share"
DEFAULT_RANKING_METRIC = "low_carbon_electricity_pct"

DEFAULT_TOP_N_RANKING = 10
DEFAULT_THEME_MODE = "Dark"


# --------------------------------------------------
# Chart style
# --------------------------------------------------
# COLOUR_SCALE is used for maps and continuous colour encodings.

COLOUR_SCALE = "YlGnBu"

# Kept for compatibility if older code still imports it.
PLOTLY_TEMPLATE = "plotly_white"