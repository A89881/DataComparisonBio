import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

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
hormone_columns = [col for col in hormone_columns if col not in ["Trip_Number", "Sample_Type"]]  # Exclude non-hormone columns

# Set seaborn style
sns.set_style("whitegrid")

# Define distinct colors for better clarity
color_palette = sns.color_palette("tab10", n_colors=df["Sample_Type"].nunique())

# Function to group, describe, print stats, and plot data
def print_boxplot_stats(data, hormone, label, ax):
    # Group by Sample_Type and Trip_Number, storing all values in a sorted list
    grouped_values = (
        data.groupby(["Sample_Type", "Trip_Number"])[hormone]
        .apply(lambda x: sorted(x.tolist()))  # Ensure sorting before visualization
        .reset_index()
    )

    # Compute descriptive statistics for each group
    grouped_values["Min"] = grouped_values[hormone].apply(lambda x: min(x))
    grouped_values["Median"] = grouped_values[hormone].apply(lambda x: np.median(x))
    grouped_values["Q3"] = grouped_values[hormone].apply(lambda x: np.percentile(x, 75))
    grouped_values["Max"] = grouped_values[hormone].apply(lambda x: max(x))

    # Print descriptive statistics for terminal output
    print(f"\nDescriptive Statistics for {label} Samples - {hormone}:")
    print(grouped_values[["Sample_Type", "Trip_Number", "Min", "Median", "Q3", "Max"]])

    # Convert lists to separate rows for seaborn compatibility
    grouped_values[hormone] = grouped_values[hormone].apply(lambda x: list(x) if isinstance(x, list) else [x])
    exploded_data = grouped_values.explode(hormone, ignore_index=True)


    # Create boxplot using correctly grouped values
    sns.boxplot(ax=ax, data=exploded_data, x="Trip_Number", y=hormone, hue="Sample_Type",
                palette=color_palette, fliersize=3, linewidth=1, width=0.5)

    # Set subplot title
    ax.set_title(f"{label} Samples - {hormone}", fontsize=14, fontweight='bold')
    ax.set_xlabel("Trip Number", fontsize=12)
    ax.set_ylabel(f"{hormone} Concentration in DW", fontsize=12)

    # Ensure legend is outside
    ax.legend(title="Sample Types", loc="upper center", bbox_to_anchor=(0.5, -0.15), ncol=3)

    # Enable independent y-axis scaling
    ax.set_ylim(exploded_data[hormone].min() * 0.9, exploded_data[hormone].max() * 1.1)

# Ensure output directory exists
plot_dir = "Statistics/Plots/"
os.makedirs(plot_dir, exist_ok=True)

# Loop through each hormone and create separate subplots
for hormone in hormone_columns:
    fig, axes = plt.subplots(1, 2, figsize=(16, 6), sharey=False)  # Two subplots, independent scales
    
    # Separate control and treated data
    control_data = df[df["Control"]]
    treated_data = df[~df["Control"]]

    # Print stats and plot control and treated samples
    print_boxplot_stats(control_data, hormone, "Control", axes[0])
    print_boxplot_stats(treated_data, hormone, "Hormone-Treated", axes[1])

    # Adjust layout and show plot
    plt.tight_layout()
    # plot_path = os.path.join(plot_dir, f"{hormone}_Boxplot.png")
    # plt.savefig(plot_path, dpi=300)
    plt.show()

"""
Quick autosave version
"""
# Loop through each hormone and create separate subplots (saving version)
# for hormone in hormone_columns:
#     fig, axes = plt.subplots(1, 2, figsize=(16, 6), sharey=False)  # Two subplots, independent scales
    
#     # Separate control and treated data
#     control_data = df[df["Control"]]
#     treated_data = df[~df["Control"]]

#     # Print stats and plot control and treated samples
#     print_boxplot_stats(control_data, hormone, "Control", axes[0])
#     print_boxplot_stats(treated_data, hormone, "Hormone-Treated", axes[1])

#     # Adjust layout
#     plt.tight_layout()

#     # Save the plot instead of showing it
#     plot_path = os.path.join(plot_dir, f"{hormone}_Boxplot.png")
#     plt.savefig(plot_path, dpi=300)
#     plt.close()

#     print(f"Saved plot: {plot_path}")
