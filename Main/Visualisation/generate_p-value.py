import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Load the dataset
file_path = "Statistics/Non-Parameteric_Analysis_Results.csv"
df = pd.read_csv(file_path)

# Filter for Trip 1 to 4
df = df[df["Trip"].between(1, 4)]

# Ensure p-values are numeric (handle possible errors)
df["p-value"] = pd.to_numeric(df["p-value"], errors="coerce")

# Create output directory
output_dir = "Statistics/Plots/p-ValuePlots"
os.makedirs(output_dir, exist_ok=True)

# Define a consistent color palette for Sample Types using "tab10"
unique_sample_types = df["Sample Type"].unique()
color_palette = sns.color_palette("tab10", n_colors=len(unique_sample_types))

# Map each Sample Type to a specific color
sample_type_colors = {sample: color for sample, color in zip(unique_sample_types, color_palette)}

# Iterate through unique hormones and generate plots
for hormone in df["Hormone"].unique():
    plt.figure(figsize=(8, 6))

    # Filter data for the current hormone
    hormone_df = df[df["Hormone"] == hormone]

    # Create barplot with consistent sample-type colors
    ax = sns.barplot(
        data=hormone_df,
        x="Trip",
        y="p-value",
        hue="Sample Type",
        palette=sample_type_colors  # Apply predefined color mapping
    )

    # Add significance threshold line (p = 0.05)
    plt.axhline(y=0.05, color="red", linestyle="--", label="Significance Threshold (p=0.05)")

    # Labels and title
    plt.xlabel("Trip")
    plt.ylabel("p-value")
    plt.title(f"P-values for {hormone}")
    plt.legend(title="Sample Type", bbox_to_anchor=(1.05, 1), loc="upper left")

    # Save the figure
    plot_path = os.path.join(output_dir, f"p_values_{hormone}.png")
    plt.savefig(plot_path, bbox_inches="tight")
    plt.close()  # Close to prevent overlapping figures

print(f"Plots saved in {output_dir}")
