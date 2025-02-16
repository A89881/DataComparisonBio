"""
Box plot with quartiles and error bars but nan for some reason
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load cleaned dataset
df = pd.read_csv("Main/Cleaned_DatasetBio.csv", delimiter=";")

# Ensure Trip_Number is numeric
df["Trip_Number"] = pd.to_numeric(df["Trip_Number"], errors="coerce")

# Extract numeric part of Sample_Name to create Sample_Type
df["Sample_Type"] = df["Sample_Name"].str.extract(r"(\d{3})")[0].astype(str)

# Identify control and hormone-treated samples
df["Control"] = df["Sample_Name"].str.startswith("K")  # Control samples start with "K"

# Identify numeric hormone columns
numeric_cols = df.select_dtypes(include=["float64", "int64"]).columns.tolist()

# Set seaborn style with more aesthetic tweaks
sns.set(style="whitegrid", palette="muted")

# Loop through each hormone and create separate subplots
for hormone in numeric_cols:
    fig, axes = plt.subplots(1, 2, figsize=(16, 8), sharey=True)  # Two subplots side by side

    # Separate control and treated data
    control_data = df[df["Control"]].copy()
    treated_data = df[~df["Control"]].copy()

    # Convert 'Trip_Number' to categorical for correct boxplot grouping
    control_data["Trip_Number"] = control_data["Trip_Number"].astype(str)
    treated_data["Trip_Number"] = treated_data["Trip_Number"].astype(str)

    # Define boxplot settings (adjusting box width, linewidth, and removing fliers)
    boxplot_kwargs = dict(width=0.6, linewidth=1.5, showfliers=False, boxprops=dict(alpha=0.7))

    # Plot Control Data (Left subplot)
    sns.boxplot(ax=axes[0], data=control_data, x="Trip_Number", y=hormone, hue="Sample_Type", palette="Set2", **boxplot_kwargs)
    axes[0].set_title(f"Control Samples - {hormone}", fontsize=16, fontweight="bold")
    # axes[0].set_xlabel("Trip Number (A=1, B=2, C=3, D=4)", fontsize=14)
    axes[0].set_ylabel(f"{hormone} Concentration (ngH/g FW or DW)", fontsize=14)
    axes[0].tick_params(axis='both', labelsize=12)

    # Plot Hormone-Treated Data (Right subplot)
    sns.boxplot(ax=axes[1], data=treated_data, x="Trip_Number", y=hormone, hue="Sample_Type", palette="Set3", **boxplot_kwargs)
    axes[1].set_title(f"Hormone-Treated Samples - {hormone}", fontsize=16, fontweight="bold")
    # axes[1].set_xlabel("Trip Number (A=1, B=2, C=3, D=4)", fontsize=14)
    axes[1].tick_params(axis='both', labelsize=12)

    # Auto-scale y-axis
    axes[0].autoscale()
    axes[1].autoscale()

    # Move legends inside the plot area (to avoid clutter)
    sns.move_legend(axes[0], "lower center", bbox_to_anchor=(0.5, -0.2), ncol=6, title="Sample Types", frameon=False, fontsize=12)
    sns.move_legend(axes[1], "lower center", bbox_to_anchor=(0.5, -0.2), ncol=6, title="Sample Types", frameon=False, fontsize=12)

    # Set common y-axis limits for better comparison between control and treated samples
    y_limits = [df[hormone].min() - 0.5, df[hormone].max() + 0.5]
    axes[0].set_ylim(y_limits)
    axes[1].set_ylim(y_limits)

    # Adjust layout for better spacing
    plt.tight_layout()

    # Show the plot
    plt.show()
