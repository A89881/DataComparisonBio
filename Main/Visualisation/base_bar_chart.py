"""
Data visualisation with bar chart no error bars or etcetera
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load cleaned dataset
df = pd.read_csv("Statistics/Cleaned_DatasetBio.csv", delimiter=";")

# Ensure Trip_Number is treated as an integer
df["Trip_Number"] = df["Trip_Number"].astype(int)

# Extract numeric part of Sample_Type (removing prefixes like 'K1-' or 'GA1-')
df["Sample_Type"] = df["Sample_Name"].str.extract(r'(\d{3})')[0]  # Extracts the three-digit number

# Identify control and hormone-treated samples
df["Control"] = df["Sample_Name"].str.startswith("K")  # Control samples start with "K"

# Group by Trip_Number and Sample_Type, then compute mean hormone content
grouped_df = df.groupby(["Trip_Number", "Sample_Type", "Control"]).median(numeric_only=True).reset_index()

# Set seaborn style
sns.set_style("whitegrid")

# Get list of hormone columns (excluding metadata)
hormone_columns = df.columns[2:-4]  # Adjust index slicing as needed

# Define distinct colors for better clarity
color_palette = sns.color_palette("tab10", n_colors=len(grouped_df["Sample_Type"].unique()))

# Loop through each hormone and create separate subplots
for hormone in hormone_columns:
    fig, axes = plt.subplots(1, 2, figsize=(16, 6), sharey=True)  # Two subplots side by side
    
    # Separate control and treated data
    control_data = grouped_df[grouped_df["Control"]]
    treated_data = grouped_df[~grouped_df["Control"]]
    
    # Plot Control Data (Left subplot)
    ax1 = sns.barplot(ax=axes[0], data=control_data, x="Trip_Number", y=hormone, hue="Sample_Type", palette=color_palette)
    axes[0].set_title(f"Control Samples - {hormone}", fontsize=14, fontweight='bold')
    axes[0].set_xlabel("Trip Number (A=1, B=2, C=3, D=4)", fontsize=12)
    axes[0].set_ylabel(f"{hormone} Concentration (ngH/g FW or DW)", fontsize=12)
    
    # Plot Hormone-Treated Data (Right subplot)
    ax2 = sns.barplot(ax=axes[1], data=treated_data, x="Trip_Number", y=hormone, hue="Sample_Type", palette=color_palette)
    axes[1].set_title(f"Hormone-Treated Samples - {hormone}", fontsize=14, fontweight='bold')
    axes[1].set_xlabel("Trip Number (A=1, B=2, C=3, D=4)", fontsize=12)
    
   # Move legends inside their respective subplots
    sns.move_legend(ax1, "lower center", bbox_to_anchor=(.5, -0.25), ncol=6, title="Sample Types", frameon=False)
    sns.move_legend(ax2, "lower center", bbox_to_anchor=(.5, -0.25), ncol=6, title="Sample Types", frameon=False)

    # Adjust layout to fit legends properly
    plt.tight_layout()
    plt.show()
