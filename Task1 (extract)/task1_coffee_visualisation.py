"""
Task 1 - CoffeeAndCode Static Visualisation
Assessment 3: One Static Visualisation and Design Report

Research question:
How do daily coding hours vary by age group and ability to code without coffee?

This script creates a static heatmap using the CoffeeAndCode dataset.

The visualisation uses:
- CodingHours as the quantitative variable
- AgeRange as a categorical variable on the x-axis
- CodingWithoutCoffee as a categorical variable on the y-axis
- Colour intensity to show average daily coding hours
- Cell labels to show the average and the number of respondents

Outputs:
1. task1_coffeeandcode_static_heatmap.png
2. task1_coffeeandcode_grouped_summary.csv
3. task1_coffeeandcode_data_cleaning_notes.txt

How to run in VS Code:
1. Put this Python file in the same folder as CoffeeAndCode.csv
2. Open the folder in VS Code
3. Run these commands in the terminal:

   python3 -m pip install pandas matplotlib numpy
   python3 task1_coffeeandcode_static_heatmap.py
"""

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# --------------------------------------------------
# 1. File paths
# --------------------------------------------------

CSV_FILE = Path("CoffeeAndCode.csv")

OUTPUT_IMAGE = Path("task1_coffeeandcode_static_heatmap.png")
OUTPUT_SUMMARY = Path("task1_coffeeandcode_grouped_summary.csv")
OUTPUT_CLEANING_NOTES = Path("task1_coffeeandcode_data_cleaning_notes.txt")


# --------------------------------------------------
# 2. Load the dataset
# --------------------------------------------------

if not CSV_FILE.exists():
    raise FileNotFoundError(
        "Could not find CoffeeAndCode.csv. "
        "Make sure this Python file is saved in the same folder as the CSV file."
    )

df = pd.read_csv(CSV_FILE)

# Remove accidental spaces from column names
df.columns = df.columns.str.strip()


# --------------------------------------------------
# 3. Check required columns
# --------------------------------------------------

required_columns = [
    "CodingHours",
    "AgeRange",
    "CodingWithoutCoffee",
]

missing_columns = [column for column in required_columns if column not in df.columns]

if missing_columns:
    raise ValueError(
        f"The following required columns are missing from the dataset: {missing_columns}"
    )


# --------------------------------------------------
# 4. Clean and prepare the data
# --------------------------------------------------

data = df.copy()

original_row_count = len(data)

# Convert the quantitative variable to numeric
data["CodingHours"] = pd.to_numeric(data["CodingHours"], errors="coerce")

# Standardise categorical variables
data["AgeRange"] = data["AgeRange"].fillna("Not stated").astype(str).str.strip()
data["CodingWithoutCoffee"] = (
    data["CodingWithoutCoffee"]
    .fillna("Not stated")
    .astype(str)
    .str.strip()
)

# Treat common missing-value labels as "Not stated"
missing_labels = ["NA", "N/A", "nan", "NaN", "None", ""]
data["AgeRange"] = data["AgeRange"].replace(missing_labels, "Not stated")
data["CodingWithoutCoffee"] = data["CodingWithoutCoffee"].replace(
    missing_labels,
    "Not stated"
)

# Remove rows where CodingHours is missing
before_missing_coding_hours = len(data)
data = data.dropna(subset=["CodingHours"])
removed_missing_coding_hours = before_missing_coding_hours - len(data)

# Remove unrealistic coding-hour values
# The assessment description gives CodingHours as approximately 1–12 hours.
before_range_filter = len(data)
data = data[(data["CodingHours"] >= 0) & (data["CodingHours"] <= 12)]
removed_out_of_range = before_range_filter - len(data)

# Remove rows where AgeRange is not stated
# This keeps the final visual focused on meaningful age-group comparison.
before_age_filter = len(data)
data = data[data["AgeRange"] != "Not stated"]
removed_not_stated_age = before_age_filter - len(data)

# Remove rows where CodingWithoutCoffee is not one of the expected answers
valid_coffee_dependence = ["Yes", "Sometimes", "No"]

before_dependence_filter = len(data)
data = data[data["CodingWithoutCoffee"].isin(valid_coffee_dependence)]
removed_invalid_dependence = before_dependence_filter - len(data)


# --------------------------------------------------
# 5. Define category order
# --------------------------------------------------

age_order = [
    "Under 18",
    "18 to 29",
    "30 to 39",
    "40 to 49",
    "50 to 59",
]

coffee_dependence_order = [
    "Yes",
    "Sometimes",
    "No",
]

# Keep only categories that are present after cleaning
age_order_present = [
    age for age in age_order if age in data["AgeRange"].unique()
]

coffee_dependence_order_present = [
    answer for answer in coffee_dependence_order
    if answer in data["CodingWithoutCoffee"].unique()
]

data["AgeRange"] = pd.Categorical(
    data["AgeRange"],
    categories=age_order_present,
    ordered=True
)

data["CodingWithoutCoffee"] = pd.Categorical(
    data["CodingWithoutCoffee"],
    categories=coffee_dependence_order_present,
    ordered=True
)


# --------------------------------------------------
# 6. Group the data for the heatmap
# --------------------------------------------------

summary = (
    data.groupby(
        ["CodingWithoutCoffee", "AgeRange"],
        observed=True
    )
    .agg(
        AverageCodingHours=("CodingHours", "mean"),
        Respondents=("CodingHours", "size")
    )
    .reset_index()
)

# Save the grouped summary for transparency and report writing
summary.to_csv(OUTPUT_SUMMARY, index=False)


# --------------------------------------------------
# 7. Create heatmap matrices
# --------------------------------------------------

average_matrix = (
    summary
    .pivot(
        index="CodingWithoutCoffee",
        columns="AgeRange",
        values="AverageCodingHours"
    )
    .reindex(
        index=coffee_dependence_order_present,
        columns=age_order_present
    )
)

count_matrix = (
    summary
    .pivot(
        index="CodingWithoutCoffee",
        columns="AgeRange",
        values="Respondents"
    )
    .reindex(
        index=coffee_dependence_order_present,
        columns=age_order_present
    )
)


# --------------------------------------------------
# 8. Create the static heatmap
# --------------------------------------------------

fig, ax = plt.subplots(figsize=(15.5, 7))

# Mask empty cells so combinations with no data appear clearly
masked_values = np.ma.masked_invalid(average_matrix.values)

# Use a readable colour scale
cmap = plt.cm.viridis.copy()
cmap.set_bad(color="#f7f7f7")

heatmap = ax.imshow(
    masked_values,
    cmap=cmap,
    aspect="auto"
)


# --------------------------------------------------
# 9. Add cell labels
# --------------------------------------------------

minimum_value = np.nanmin(average_matrix.values)
maximum_value = np.nanmax(average_matrix.values)
midpoint = (minimum_value + maximum_value) / 2

for row_index in range(average_matrix.shape[0]):
    for column_index in range(average_matrix.shape[1]):

        average_value = average_matrix.iloc[row_index, column_index]
        respondent_count = count_matrix.iloc[row_index, column_index]

        if pd.isna(average_value):
            label = "—"
            text_colour = "black"
            font_weight = "normal"
        else:
            label = f"{average_value:.1f}h\n({int(respondent_count)} resp.)"

            # Low values appear on darker colours in viridis, so use white text there.
            text_colour = "white" if average_value < midpoint else "black"
            font_weight = "bold"

        ax.text(
            column_index,
            row_index,
            label,
            ha="center",
            va="center",
            fontsize=10.5,
            color=text_colour,
            fontweight=font_weight
        )


# --------------------------------------------------
# 10. Add title, subtitle, and axis labels
# --------------------------------------------------

ax.set_title(
    "How Coding Hours Vary by Age Group and Coffee Dependence",
    fontsize=18,
    fontweight="bold",
    pad=22
)

fig.text(
    0.5,
    0.91,
    "Cell colour shows average daily coding hours; labels show the average and number of respondents.",
    ha="center",
    fontsize=10.8
)

ax.set_xlabel(
    "Age range",
    fontsize=12,
    labelpad=12
)

ax.set_ylabel(
    "Can code without coffee?",
    fontsize=12,
    labelpad=12
)

ax.set_xticks(range(len(age_order_present)))
ax.set_xticklabels(
    age_order_present,
    rotation=20,
    ha="right",
    fontsize=11
)

ax.set_yticks(range(len(coffee_dependence_order_present)))
ax.set_yticklabels(
    coffee_dependence_order_present,
    fontsize=11
)


# --------------------------------------------------
# 11. Add custom grid lines
# --------------------------------------------------

number_of_rows = len(coffee_dependence_order_present)
number_of_columns = len(age_order_present)

# Remove default grid
ax.grid(False)

# Horizontal separators between y-axis values
# These are lighter so they separate rows without dominating the chart.
for y_position in np.arange(-0.5, number_of_rows + 0.5, 1):
    ax.hlines(
        y_position,
        -0.5,
        number_of_columns - 0.5,
        colors="#b5b5b5",
        linewidth=3.0
    )

# Vertical separators between age groups
# These are darker to clearly separate the age categories.
for x_position in np.arange(-0.5, number_of_columns + 0.5, 1):
    ax.vlines(
        x_position,
        -0.5,
        number_of_rows - 0.5,
        colors="black",
        linewidth=3.2
    )


# --------------------------------------------------
# 12. Add colour bar
# --------------------------------------------------

colour_bar = fig.colorbar(
    heatmap,
    ax=ax
)

colour_bar.set_label(
    "Average coding hours per day",
    fontsize=10.5
)


# --------------------------------------------------
# 13. Add explanatory note
# --------------------------------------------------

fig.text(
    0.5,
    0.025,
    "Note: resp. = respondents in each group. Empty cells represent category combinations with no responses.",
    ha="center",
    fontsize=9.5,
    style="italic"
)


# --------------------------------------------------
# 14. Save data-cleaning notes
# --------------------------------------------------

cleaning_notes = f"""
Task 1 CoffeeAndCode Data Cleaning Notes

Original number of rows:
{original_row_count}

Rows removed because CodingHours was missing:
{removed_missing_coding_hours}

Rows removed because CodingHours was outside the expected 0–12 range:
{removed_out_of_range}

Rows removed because AgeRange was not stated:
{removed_not_stated_age}

Rows removed because CodingWithoutCoffee was missing or outside the expected categories:
{removed_invalid_dependence}

Final number of rows used in the visualisation:
{len(data)}

Variables used in the final visualisation:
- CodingHours: quantitative variable, aggregated as average daily coding hours
- AgeRange: categorical variable shown on the x-axis
- CodingWithoutCoffee: categorical variable shown on the y-axis

Design note:
The heatmap was selected because it supports comparison across two categorical variables while using colour intensity to represent a quantitative measure. Cell labels show both the average coding hours and the number of respondents, which helps prevent small groups from being overinterpreted.
"""

OUTPUT_CLEANING_NOTES.write_text(cleaning_notes.strip(), encoding="utf-8")


# --------------------------------------------------
# 15. Save and show the visualisation
# --------------------------------------------------

plt.tight_layout(rect=[0, 0.07, 1, 0.86])

fig.savefig(
    OUTPUT_IMAGE,
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print(f"Static visualisation saved as: {OUTPUT_IMAGE.resolve()}")
print(f"Grouped summary saved as: {OUTPUT_SUMMARY.resolve()}")
print(f"Data-cleaning notes saved as: {OUTPUT_CLEANING_NOTES.resolve()}")