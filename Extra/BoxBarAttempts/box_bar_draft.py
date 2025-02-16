"""Stastical csv code"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load cleaned dataset
df = pd.read_csv("Main/Cleaned_DatasetBio.csv", delimiter=";")

# Ensure Trip_Number is treated as an integer
df["Trip_Number"] = df["Trip_Number"].astype(int)

# Extract numeric part of Sample_Type (removing prefixes like 'K1-' or 'GA1-')
df["Sample_Type"] = df["Sample_Name"].str.extract(r'(\d{3})')[0]  # Extracts the three-digit number

# Identify control and hormone-treated samples
df["Control"] = df["Sample_Name"].str.startswith("K")  # Control samples start with "K"

# Group by Trip_Number and Sample_Type, then compute median hormone content
grouped_df = df.groupby(["Trip_Number", "Sample_Type", "Control"]).mean(numeric_only=True).reset_index()

# Set seaborn style
sns.set_style("whitegrid")

# Get list of hormone columns (excluding metadata)
hormone_columns = df.columns[2:-4]  # Adjust index slicing as needed

# Define distinct colors for better clarity
color_palette = sns.color_palette("tab10", n_colors=len(grouped_df["Sample_Type"].unique()))

# Dataframe for statistical summaries
summary_stats = []

# Loop through each hormone and create separate subplots
for hormone in hormone_columns:
    fig, axes = plt.subplots(1, 2, figsize=(16, 6), sharey=True)  # Two subplots side by side
    
    # Separate control and treated data
    control_data = grouped_df[grouped_df["Control"]]
    treated_data = grouped_df[~grouped_df["Control"]]
    
    # Plot Control Data (Left subplot)
    ax1 = sns.boxplot(ax=axes[0], data=control_data, y=hormone, hue="Sample_Type",
                      palette=color_palette, fliersize=3, linewidth=1, width=0.5)
    axes[0].set_title(f"Control Samples - {hormone}", fontsize=14, fontweight='bold')
    axes[0].set_ylabel(f"{hormone} Concentration (ngH/g FW or DW)", fontsize=12)
    
    # Plot Hormone-Treated Data (Right subplot)
    ax2 = sns.boxplot(ax=axes[1], data=treated_data, y=hormone, hue="Sample_Type",
                      palette=color_palette, fliersize=3, linewidth=1, width=0.5)
    axes[1].set_title(f"Hormone-Treated Samples - {hormone}", fontsize=14, fontweight='bold')
    
    # Move legends inside their respective subplots
    sns.move_legend(ax1, "lower center", bbox_to_anchor=(.5, -0.25), ncol=6, title="Sample Types", frameon=False)
    sns.move_legend(ax2, "lower center", bbox_to_anchor=(.5, -0.25), ncol=6, title="Sample Types", frameon=False)

    # Adjust layout to fit legends properly
    plt.tight_layout()
    plt.show()
    
#     # Calculate statistics
#     for control in [True, False]:
#         group_data = grouped_df[grouped_df["Control"] == control]
        
#         for sample_type in group_data["Sample_Type"].unique():
#             sample_data = group_data[group_data["Sample_Type"] == sample_type][hormone]
            
#             # Statistics
#             mean_val = sample_data.mean()
#             median_val = sample_data.median()
#             std_dev = sample_data.std()
#             quartiles = sample_data.quantile([0.25, 0.5, 0.75])
            
#             # Reliability and Statistical Average (mean/standard deviation ratio)
#             reliability = mean_val / std_dev if std_dev != 0 else 0
#             stat_avg = (mean_val + median_val) / 2
            
#             # Append to summary list
#             summary_stats.append({
#                 "Sample_Type": sample_type,
#                 "Control": "Control" if control else "Hormone-Treated",
#                 "Mean": mean_val,
#                 "Median": median_val,
#                 "Standard Deviation": std_dev,
#                 "25th Percentile": quartiles[0.25],
#                 "50th Percentile (Median)": quartiles[0.5],
#                 "75th Percentile": quartiles[0.75],
#                 "Reliability": reliability,
#                 "Statistical Average": stat_avg
#             })

# # Convert summary stats into a DataFrame
# summary_df = pd.DataFrame(summary_stats)

# # Save to CSV
# summary_df.to_csv("Sample_Type_Statistics.csv", index=False)
