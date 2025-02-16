# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
# import numpy as np

# # Load cleaned dataset
# df = pd.read_csv("Main/Cleaned_DatasetBio.csv", delimiter=";")

# # Ensure Trip_Number is treated as an integer
# df["Trip_Number"] = df["Trip_Number"].astype(int)

# # Extract Sample_Type from Sample_Name
# df["Sample_Type"] = df["Sample_Name"].str.extract(r'(\d{3})')[0]
# df = df.dropna(subset=["Sample_Type"])  # Remove NaN rows
# df["Sample_Type"] = df["Sample_Type"].astype(int)

# # Identify control and hormone-treated samples
# df["Control"] = df["Sample_Name"].str.startswith("K")  # Control samples start with "K"

# # Get hormone columns explicitly
# hormone_columns = df.select_dtypes(include=["float64", "int64"]).columns.tolist()
# print(hormone_columns)

# # Set seaborn style
# sns.set_style("whitegrid")

# # Define distinct colors for better clarity
# color_palette = sns.color_palette("tab10", n_colors=df["Sample_Type"].nunique())

# # Function to group, describe, and plot data
# def print_boxplot_stats(data, hormone, label, ax):
#     # Group by Sample_Type and Trip_Number, storing all values in a sorted list
#     grouped_values = (
#         data.groupby(["Sample_Type", "Trip_Number"])[hormone]
#         .apply(lambda x: sorted(x.tolist()))  # Ensure sorting before visualization
#         .reset_index()
#     )

#     # Convert lists to separate rows for seaborn compatibility
#     exploded_data = grouped_values.explode(hormone)  # Expands lists into separate rows

#     # Convert hormone values back to float (they become objects after explode)
#     exploded_data[hormone] = exploded_data[hormone].astype(float)

#     # Create boxplot using correctly grouped values
#     sns.boxplot(ax=ax, data=exploded_data, x="Trip_Number", y=hormone, hue="Sample_Type",
#                 palette=color_palette, fliersize=3, linewidth=1, width=0.5)

#     # Set subplot title
#     ax.set_title(f"{label} Samples - {hormone}", fontsize=14, fontweight='bold')
#     ax.set_xlabel("Trip Number", fontsize=12)
#     ax.set_ylabel(f"{hormone} Concentration", fontsize=12)

#     # Ensure legend is outside
#     ax.legend(title="Sample Types", loc="upper center", bbox_to_anchor=(0.5, -0.15), ncol=3)

# # Loop through each hormone and create separate subplots
# for hormone in hormone_columns:
#     print(hormone)
#     fig, axes = plt.subplots(1, 2, figsize=(16, 6), sharey=True)  # Two subplots side by side
    
#     # Separate control and treated data
#     control_data = df[df["Control"]]
#     treated_data = df[~df["Control"]]

#     # Plot control and treated samples
#     print_boxplot_stats(control_data, hormone, "Control", axes[0])
#     print_boxplot_stats(treated_data, hormone, "Hormone-Treated", axes[1])

#     # Adjust layout and show plot
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

# Extract Sample_Type from Sample_Name
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

# Function to group, describe, print stats, and plot data
def print_boxplot_stats(data, hormone, label, ax):
    # Group by Sample_Type and Trip_Number, storing all values in a sorted list
    grouped_values = (
        data.groupby(["Sample_Type", "Trip_Number"])[hormone]
        .apply(lambda x: sorted(x.tolist()))  # Ensure sorting before visualization
        .reset_index()
    )

    # Compute descriptive statistics for each group
    grouped_values["Median"] = grouped_values[hormone].apply(lambda x: np.median(x))
    grouped_values["Min"] = grouped_values[hormone].apply(lambda x: min(x))
    grouped_values["Max"] = grouped_values[hormone].apply(lambda x: max(x))
    grouped_values["Q1"] = grouped_values[hormone].apply(lambda x: np.percentile(x, 25))
    grouped_values["Q3"] = grouped_values[hormone].apply(lambda x: np.percentile(x, 75))

    # Print descriptive statistics for terminal output
    print(f"\nDescriptive Statistics for {label} Samples - {hormone}:")
    print(grouped_values[["Sample_Type", "Trip_Number", "Median", "Min", "Q1", "Q3", "Max"]])

    # Convert lists to separate rows for seaborn compatibility
    exploded_data = grouped_values.explode(hormone)  # Expands lists into separate rows

    # Convert hormone values back to float (they become objects after explode)
    exploded_data[hormone] = exploded_data[hormone].astype(float)

    # Create boxplot using correctly grouped values
    sns.boxplot(ax=ax, data=exploded_data, x="Trip_Number", y=hormone, hue="Sample_Type",
                palette=color_palette, fliersize=3, linewidth=1, width=0.5)

    # Set subplot title
    ax.set_title(f"{label} Samples - {hormone}", fontsize=14, fontweight='bold')
    ax.set_xlabel("Trip Number", fontsize=12)
    ax.set_ylabel(f"{hormone} Concentration", fontsize=12)

    # Ensure legend is outside
    ax.legend(title="Sample Types", loc="upper center", bbox_to_anchor=(0.5, -0.15), ncol=3)

# Loop through each hormone and create separate subplots
for hormone in hormone_columns:
    print(hormone)
    fig, axes = plt.subplots(1, 2, figsize=(16, 6), sharey=True)  # Two subplots side by side
    
    # Separate control and treated data
    control_data = df[df["Control"]]
    treated_data = df[~df["Control"]]

    # Print stats and plot control and treated samples
    print_boxplot_stats(control_data, hormone, "Control", axes[0])
    print_boxplot_stats(treated_data, hormone, "Hormone-Treated", axes[1])

    # Adjust layout and show plot
    plt.tight_layout()
    plt.show()
