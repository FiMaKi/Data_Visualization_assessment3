# Assessment 3: Data Visualisation

This repository contains the files for Assessment 3.

## Task 1: Static Visualisation

Task 1 uses the CoffeeAndCode dataset to create a static heatmap showing how daily coding hours vary by age group and ability to code without coffee.

Files:
- `task1/CoffeeAndCode.csv`
- `task1/task1_coffee_visualisation.py`
- `task1/task1_coffeeandcode_static_heatmap.png`
- `task1/task1_coffeeandcode_grouped_summary.csv`
- `task1/task1_coffeeandcode_data_cleaning_notes.txt`

## Task 2: Interactive Dashboard

Task 2 is a Streamlit dashboard using the Global Sustainable Energy dataset. It explores electricity access, clean fuel access, renewable energy share, electricity generation mix, GDP per capita, and CO2 emissions per capita.

Files:
- `task2/app.py`
- `task2/config.py`
- `task2/data_loader.py`
- `task2/helpers.py`
- `task2/sidebar.py`
- `task2/ui_components.py`
- `task2/visuals.py`
- `task2/requirements.txt`
- `task2/global-data-on-sustainable-energy.csv`

## How to run Task 2

```bash
cd task2
python3 -m pip install -r requirements.txt
python3 -m streamlit run app.py
