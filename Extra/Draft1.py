import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load cleaned dataset
df = pd.read_csv("Main\Cleaned_DatasetBio.csv", delimiter=";")

# Ensure Trip_Number is treated as a category
df["Trip_Number"] = df["Trip_Number"].astype(int)

# Extract sample type without trip letter (e.g., "K1-171" from "K1-171-A")
df["Sample_Type"] = df["Sample_Name"].str.rsplit("-", n=1).str[0]

# Group by Sample_Type and Trip_Number, then compute mean hormone content
grouped_df = df.groupby(["Trip_Number", "Sample_Type"]).mean(numeric_only=True).reset_index()

# Set visualization style
sns.set_style("whitegrid")

# Get list of hormone columns (excluding metadata)
hormone_columns = df.columns[2:-4]  # Adjust index slicing as needed

# Plot each hormone separately
for hormone in hormone_columns:
    plt.figure(figsize=(10, 6))
    
    # Create barplot
    sns.barplot(data=grouped_df, x="Trip_Number", y=hormone, hue="Sample_Type", palette="viridis")
    
    # Titles and labels
    plt.title(f"Average {hormone} Concentration per Trip and Sample Type")
    plt.xlabel("Trip Number (A=1, B=2, C=3, D=4)")
    plt.ylabel(f"{hormone} Concentration")
    plt.legend(title="Sample Type", bbox_to_anchor=(1.05, 1), loc='upper left')
    
    # Show graph
    plt.show()
