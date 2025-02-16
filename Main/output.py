import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load cleaned dataset
df = pd.read_csv("Main/Cleaned_DatasetBio.csv", delimiter=";")

# Ensure Trip_Number is treated as an integer
df["Trip_Number"] = df["Trip_Number"].astype(int)

# Extract Sample_Type from Sample_Name
df["Sample_Type"] = df["Sample_Name"].str.extract(r'(\d{3})')[0]
df = df.dropna(subset=["Sample_Type"])  # Remove NaN rows
df["Sample_Type"] = df["Sample_Type"].astype(int)

# Identify control and hormone-treated samples
df["Control"] = df["Sample_Name"].str.startswith("K")  # Control samples start with "K"

# Get hormone columns explicitly
hormone_columns = df.select_dtypes(include=["float64", "int64"]).columns.tolist()

# Set seaborn style
sns.set_style("whitegrid")

# Define distinct colors for better clarity
color_palette = sns.color_palette("tab10", n_colors=df["Sample_Type"].nunique())

# Output file for descriptive statistics
output_file = "descriptive_statistics.txt"

# Function to compute stats and write side-by-side output
def write_boxplot_stats(control_data, treated_data, hormone):
    # Compute descriptive stats for Control samples
    control_stats = (
        control_data.groupby(["Sample_Type", "Trip_Number"])[hormone]
        .apply(lambda x: sorted(x.tolist()))  # Ensure sorting
        .reset_index()
    )
    control_stats["Min"] = control_stats[hormone].apply(min)
    control_stats["Median"] = control_stats[hormone].apply(np.median)
    control_stats["Q3"] = control_stats[hormone].apply(lambda x: np.percentile(x, 75))
    control_stats["Max"] = control_stats[hormone].apply(max)
    control_stats = control_stats.drop(columns=[hormone])  # Drop original value column

    # Compute descriptive stats for Hormone-Treated samples
    treated_stats = (
        treated_data.groupby(["Sample_Type", "Trip_Number"])[hormone]
        .apply(lambda x: sorted(x.tolist()))  # Ensure sorting
        .reset_index()
    )
    treated_stats["Min"] = treated_stats[hormone].apply(min)
    treated_stats["Median"] = treated_stats[hormone].apply(np.median)
    treated_stats["Q3"] = treated_stats[hormone].apply(lambda x: np.percentile(x, 75))
    treated_stats["Max"] = treated_stats[hormone].apply(max)
    treated_stats = treated_stats.drop(columns=[hormone])  # Drop original value column

    # Merge statistics side by side
    merged_stats = pd.merge(control_stats, treated_stats, on=["Sample_Type", "Trip_Number"], suffixes=("_Control", "_Treated"), how="outer")

    # Print statistics in terminal
    print(f"\nDescriptive Statistics for {hormone}:")
    print(merged_stats.to_string(index=False))

    # Write to file
    with open(output_file, "a") as f:
        f.write(f"\nDescriptive Statistics for {hormone}:\n")
        f.write(merged_stats.to_string(index=False))
        f.write("\n" + "=" * 70 + "\n")  # Separator

# Clear previous contents of the output file
with open(output_file, "w") as f:
    f.write("Descriptive Statistics Output\n")
    f.write("=" * 70 + "\n")

# Loop through each hormone, compute stats, and plot
for hormone in hormone_columns:
    fig, axes = plt.subplots(1, 2, figsize=(16, 6), sharey=False)  # Two subplots, independent scales
    
    # Separate control and treated data
    control_data = df[df["Control"]]
    treated_data = df[~df["Control"]]

    # Compute and write side-by-side stats
    write_boxplot_stats(control_data, treated_data, hormone)

    # Create boxplots
    for data, label, ax in zip([control_data, treated_data], ["Control", "Hormone-Treated"], axes):
        exploded_data = data.explode(hormone)
        exploded_data[hormone] = exploded_data[hormone].astype(float)

        sns.boxplot(ax=ax, data=exploded_data, x="Trip_Number", y=hormone, hue="Sample_Type",
                    palette=color_palette, fliersize=3, linewidth=1, width=0.5)

        ax.set_title(f"{label} Samples - {hormone}", fontsize=14, fontweight='bold')
        ax.set_xlabel("Trip Number", fontsize=12)
        ax.set_ylabel(f"{hormone} Concentration", fontsize=12)
        ax.legend(title="Sample Types", loc="upper center", bbox_to_anchor=(0.5, -0.15), ncol=3)
        ax.set_ylim(exploded_data[hormone].min() * 0.9, exploded_data[hormone].max() * 1.1)

    # Adjust layout and show plot
    plt.tight_layout()
    plt.show()
