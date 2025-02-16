# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns

# # Load cleaned dataset
# df = pd.read_csv("Main/Cleaned_DatasetBio.csv", delimiter=";")

# # Ensure Trip_Number is treated as an integer
# df["Trip_Number"] = df["Trip_Number"].astype(int)

# df["Sample_Type"] = df["Sample_Name"].str.extract(r'(\d{3})')[0]
# df = df.dropna(subset=["Sample_Type"])  # Remove NaN rows
# df["Sample_Type"] = df["Sample_Type"].astype(int)

# # Identify control and hormone-treated samples
# df["Control"] = df["Sample_Name"].str.startswith("K")  # Control samples start with "K"

# # Get hormone columns explicitly
# hormone_columns = df.select_dtypes(include=["float64", "int64"]).columns.tolist()

# # Set seaborn style
# sns.set_style("whitegrid")

# # Define distinct colors for better clarity
# color_palette = sns.color_palette("tab10", n_colors=df["Sample_Type"].nunique())

# # Loop through each hormone and create separate subplots
# for hormone in hormone_columns:
#     fig, axes = plt.subplots(1, 2, figsize=(16, 6), sharey=True)  # Two subplots side by side
    
#     # Separate control and treated data
#     control_data = df[df["Control"]]
#     treated_data = df[~df["Control"]]

#     ## ✅ Box Plot (Corrected: Uses raw data)
#     sns.boxplot(ax=axes[0], data=control_data, x="Trip_Number", y=hormone, hue="Sample_Type",
#                 palette=color_palette, fliersize=3, linewidth=1, width=0.5)
#     axes[0].set_title(f"Control Samples - {hormone}", fontsize=14, fontweight='bold')
#     axes[0].set_ylabel(f"{hormone} Concentration (ngH/g FW or DW)", fontsize=12)

#     sns.boxplot(ax=axes[1], data=treated_data, x="Trip_Number", y=hormone, hue="Sample_Type",
#                 palette=color_palette, fliersize=3, linewidth=1, width=0.5)
#     axes[1].set_title(f"Hormone-Treated Samples - {hormone}", fontsize=14, fontweight='bold')

#     # Add legends manually
#     axes[0].legend(title="Sample Types", loc="upper right")
#     axes[1].legend(title="Sample Types", loc="upper right")

#     # Adjust layout
#     plt.tight_layout()
#     plt.show()

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load cleaned dataset
df = pd.read_csv("Main/Cleaned_DatasetBio.csv", delimiter=";")

# Ensure Trip_Number is treated as an integer
df["Trip_Number"] = df["Trip_Number"].astype(int)

df["Sample_Type"] = df["Sample_Name"].str.extract(r'(\d{3})')[0]
df = df.dropna(subset=["Sample_Type"])  # Remove NaN rows
df["Sample_Type"] = df["Sample_Type"].astype(int)

# Identify control and hormone-treated samples
df["Control"] = df["Sample_Name"].str.startswith("K")  # Control samples start with "K"

# Get hormone columns explicitly
hormone_columns = df.select_dtypes(include=["float64", "int64"]).columns.tolist()
print(hormone_columns)

# Set seaborn style
sns.set_style("whitegrid")

# Define distinct colors for better clarity
color_palette = sns.color_palette("tab10", n_colors=df["Sample_Type"].nunique())

# Loop through each hormone and create separate subplots
for hormone in hormone_columns:
    print(hormone)
    fig, axes = plt.subplots(1, 2, figsize=(16, 6), sharey=True)  # Two subplots side by side
    
    # Separate control and treated data
    control_data = df[df["Control"]]
    treated_data = df[~df["Control"]]

    ## Box Plot (Corrected: Uses raw data)
    sns.boxplot(ax=axes[0], data=control_data, x="Trip_Number", y=hormone, hue="Sample_Type",
                palette=color_palette, fliersize=3, linewidth=1, width=0.5)
    axes[0].set_title(f"Control Samples - {hormone}", fontsize=14, fontweight='bold')
    axes[0].set_ylabel(f"{hormone} Concentration (ngH/g FW or DW)", fontsize=12)

    sns.boxplot(ax=axes[1], data=treated_data, x="Trip_Number", y=hormone, hue="Sample_Type",
                palette=color_palette, fliersize=3, linewidth=1, width=0.5)
    axes[1].set_title(f"Hormone-Treated Samples - {hormone}", fontsize=14, fontweight='bold')

    # Add legend to the bottom
    axes[0].legend(title="Sample Types", loc="upper center", bbox_to_anchor=(0.5, -0.05), ncol=3)
    axes[1].legend(title="Sample Types", loc="upper center", bbox_to_anchor=(0.5, -0.05), ncol=3)




    def print_boxplot_stats(data, hormone, label):
        # Group by Sample_Type and Trip_Number, storing all values in a sorted list
        grouped_values = (
            data.groupby(["Sample_Type", "Trip_Number"])[hormone]
            .apply(lambda x: sorted(x.tolist()))  # Ensure sorting before median calculation
            .reset_index()
        )

        print(grouped_values)

        # # Print sorted lists of concentration values per Sample_Type and Trip_Number
        # print(f"\nRaw Concentration Values for {label} Samples - {hormone}:")
        # for sample_type, group in grouped_values.groupby("Sample_Type"):
        #     print(f"Sample Type {sample_type}:")
        #     for trip, values in zip(group["Trip_Number"], group[hormone]):
        #         print(f"  Trip {trip}: {values}")

        # Compute the median for each group using the correctly sorted list
        grouped_values["Median"] = grouped_values[hormone].apply(lambda x: np.median(x))
        print(grouped_values["Median"])
   
        # # Now, describe the distribution for each Sample_Type across all trips
        # stats = grouped_values.groupby("Sample_Type")["Median"].describe()

        # print(f"\nBoxplot Statistics for {label} Samples - {hormone}:")
        # print(stats[['50%', 'min', '25%', '75%', 'max']])  # Median (50%), min, Q1, Q3, max


    print_boxplot_stats(control_data, hormone, "Control")
    print_boxplot_stats(treated_data, hormone, "Hormone-Treated")

    # Adjust layout
    plt.tight_layout()
    plt.show()
