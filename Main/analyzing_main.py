# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns

# # Load cleaned dataset
# df = pd.read_csv("Main\Cleaned_DatasetBio.csv", delimiter=";")

# # Ensure Trip_Number is treated as a category
# df["Trip_Number"] = df["Trip_Number"].astype(int)

# # Extract sample type without trip letter (e.g., "K1-171" from "K1-171-A")
# df["Sample_Type"] = df["Sample_Name"].str.rsplit("-", n=1).str[0]

# # Group by Sample_Type and Trip_Number, then compute mean hormone content
# grouped_df = df.groupby(["Trip_Number", "Sample_Type"]).mean(numeric_only=True).reset_index()

# # Set visualization style
# sns.set_style("whitegrid")

# # Get list of hormone columns (excluding metadata)
# hormone_columns = df.columns[2:-4]  # Adjust index slicing as needed

# # Plot each hormone separately
# for hormone in hormone_columns:
#     plt.figure(figsize=(10, 6))
    
#     # Create barplot
#     sns.barplot(data=grouped_df, x="Trip_Number", y=hormone, hue="Sample_Type", palette="viridis")
    
#     # Titles and labels
#     plt.title(f"Average {hormone} Concentration per Trip and Sample Type")
#     plt.xlabel("Trip Number (A=1, B=2, C=3, D=4)")
#     plt.ylabel(f"{hormone} Concentration")
#     plt.legend(title="Sample Type", bbox_to_anchor=(1.05, 1), loc='upper left')
    
#     # Show graph
#     plt.show()


"""
Second Version with ''Clearer'' graph but same method
"""

# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns

# # Load cleaned dataset
# df = pd.read_csv("Main/Cleaned_DatasetBio.csv", delimiter=";")

# # Ensure Trip_Number is treated as a category
# df["Trip_Number"] = df["Trip_Number"].astype(int)

# # Extract sample type without trip letter (e.g., "K1-171" from "K1-171-A")
# df["Sample_Type"] = df["Sample_Name"].str.rsplit("-", n=1).str[0]

# # Group by Sample_Type and Trip_Number, then compute mean hormone content
# grouped_df = df.groupby(["Trip_Number", "Sample_Type"]).mean(numeric_only=True).reset_index()

# # Set visualization style
# sns.set_style("whitegrid")

# # Get list of hormone columns (excluding metadata)
# hormone_columns = df.columns[2:-4]  # Adjust index slicing as needed

# # Loop through each hormone and create separate bar plots
# for hormone in hormone_columns:
#     plt.figure(figsize=(12, 6))  # Larger figure size for visibility
    
#     # Create barplot with improved color differentiation
#     sns.barplot(data=grouped_df, x="Trip_Number", y=hormone, hue="Sample_Type", palette="Set2")
    
#     # Auto-scale y-axis based on max value with some buffer space
#     max_value = grouped_df[hormone].max()
#     plt.ylim(0, max_value * 1.2 if max_value > 0 else 1)  # Prevents all-zero cases from breaking the scale
    
#     # Titles and labels with improved visibility
#     plt.title(f"Average {hormone} Concentration per Trip and Sample Type", fontsize=14, fontweight='bold')
#     plt.xlabel("Trip Number (A=1, B=2, C=3, D=4)", fontsize=12)
#     plt.ylabel(f"{hormone} Concentration", fontsize=12)
    
#     # Improve legend visibility
#     plt.legend(title="Sample Type", bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=10)
    
#     # Show graph
#     plt.show()


import pandas as pd

# Load cleaned dataset
file_path = "Main/Cleaned_DatasetBio.csv"
df = pd.read_csv(file_path, delimiter=";")

# Ensure Trip_Number is treated as a category
df["Trip_Number"] = df["Trip_Number"].astype(int)

# Extract sample type without trip letter (e.g., "K1-171" from "K1-171-A")
df["Sample_Type"] = df["Sample_Name"].str.rsplit("-", n=1).str[0]

# Group by Sample_Type and Trip_Number, then compute mean hormone content
grouped_df = df.groupby(["Trip_Number", "Sample_Type"]).mean(numeric_only=True).reset_index()

# Get list of hormone columns (excluding metadata)
hormone_columns = df.columns[2:-4]  # Adjust index slicing as needed

# Prepare structured output
formatted_data = []

for hormone in hormone_columns:
    hormone_section = [[hormone]]  # Start with hormone name as a header
    for trip in sorted(grouped_df["Trip_Number"].unique()):
        trip_samples = grouped_df[grouped_df["Trip_Number"] == trip][["Sample_Type", hormone]]
        for _, row in trip_samples.iterrows():
            formatted_row = [row["Sample_Type"], row[hormone]]
            hormone_section.append(formatted_row)
    formatted_data.append(hormone_section)

# Convert to a structured dataframe
formatted_output = []
for section in formatted_data:
    max_length = max(len(row) for row in section)
    padded_section = [row + [""] * (max_length - len(row)) for row in section]
    formatted_output.extend(padded_section)
    formatted_output.append([])  # Blank line for separation

# Save the formatted dataset
formatted_df = pd.DataFrame(formatted_output)
formatted_csv_path = "Main/Structured_Hormone_Data.csv"
formatted_df.to_csv(formatted_csv_path, index=False, header=False, sep=";")

# Return the file path for user download
formatted_csv_path
