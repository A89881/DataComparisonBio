import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load cleaned dataset
df = pd.read_csv("Statistics/Cleaned_DatasetBio.csv", delimiter=";")

# Ensure Trip_Number is treated as an integer
df["Trip_Number"] = df["Trip_Number"].astype(int)

# Extract Sample_Type from Sample_Name
df["Sample_Type"] = df["Sample_Name"].str.extract(r'(\d{2,3})')[0]
df = df.dropna(subset=["Sample_Type"])  # Remove NaN rows
df["Sample_Type"] = df["Sample_Type"].astype(int)

# Identify control and hormone-treated samples
df["Control"] = df["Sample_Name"].str.startswith("K")  # Control samples start with "K"

# Get hormone columns explicitly
hormone_columns = df.select_dtypes(include=["float64", "int64"]).columns.tolist()

# Set seaborn style
sns.set_style("whitegrid")

# Output file for descriptive statistics
output_file = "Statistics/Standard_statistics.csv"

# Function to compute and save descriptive statistics
def compute_descriptive_stats(control_data, treated_data, hormone):
    # Compute descriptive stats for Control samples
    control_stats = control_data.groupby(["Sample_Type", "Trip_Number"])[hormone].describe()[["min", "50%", "75%", "max"]]
    control_stats = control_stats.rename(columns={"50%": "median", "75%": "Q3"})

    # Compute descriptive stats for Treated samples
    treated_stats = treated_data.groupby(["Sample_Type", "Trip_Number"])[hormone].describe()[["min", "50%", "75%", "max"]]
    treated_stats = treated_stats.rename(columns={"50%": "median", "75%": "Q3"})

    # Merge statistics side by side
    merged_stats = pd.merge(control_stats, treated_stats, on=["Sample_Type", "Trip_Number"], 
                            suffixes=("_Control", "_Treated"), how="outer")

    return merged_stats

# Prepare a list to store results for all hormones
all_stats = []

# Loop through each hormone, compute stats, and plot
for hormone in hormone_columns:
    # Separate control and treated data
    control_data = df[df["Control"]]
    treated_data = df[~df["Control"]]

    # Compute and store side-by-side stats
    stats_df = compute_descriptive_stats(control_data, treated_data, hormone)
    stats_df.insert(0, "Hormone", hormone)  # Add hormone name as first column
    all_stats.append(stats_df)

# Concatenate all statistics into one DataFrame
final_stats_df = pd.concat(all_stats)

# Save structured CSV output
final_stats_df.to_csv(output_file, index=True)

print(f"Descriptive statistics saved to {output_file}")
