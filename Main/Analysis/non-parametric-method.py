import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import mannwhitneyu, rankdata

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

# Get hormone columns explicitly (only columns that are numeric and not Trip_Number or Sample_Type)
hormone_columns = df.select_dtypes(include=["float64", "int64"]).columns.tolist()
hormone_columns = [col for col in hormone_columns if col not in ["Trip_Number", "Sample_Type"]]  # Exclude non-hormone columns

# Set seaborn style
sns.set_style("whitegrid")

# Function to compute Cliff's Delta for effect size
def cliffs_delta(x, y):
    """
    Computes Cliff's Delta effect size and categorizes it.
    Returns effect size and its categorical interpretation.
    """
    x, y = np.array(x), np.array(y)
    nx, ny = len(x), len(y)

    if nx == 0 or ny == 0:
        return np.nan, "Manual Review Needed"

    combined = np.concatenate((x, y))  
    ranks = rankdata(combined)  

    rx, ry = ranks[:nx], ranks[nx:]

    num_greater = np.sum(rx[:, None] > ry)
    num_lesser = np.sum(rx[:, None] < ry)

    delta = (num_greater - num_lesser) / (nx * ny)

    # Categorize effect size
    if abs(delta) < 0.147:
        category = "Small"
    elif abs(delta) < 0.33:
        category = "Medium"
    else:
        category = "Large"

    return round(delta, 4), category

# Function to perform Mann-Whitney U test trip by trip
def perform_statistical_analysis(df):
    """
    Performs Mann-Whitney U test for each trip, comparing Control vs. Hormone-Treated samples
    for each sample type and hormone.
    Returns a single consolidated results table.
    """
    results = []

    for hormone in hormone_columns:
        for sample_type in df["Sample_Type"].unique():
            for trip in df["Trip_Number"].unique():
                control_values = df[(df["Trip_Number"] == trip) & (df["Control"]) & (df["Sample_Type"] == sample_type)][hormone].dropna()
                treated_values = df[(df["Trip_Number"] == trip) & (~df["Control"]) & (df["Sample_Type"] == sample_type)][hormone].dropna()

                if len(control_values) < 2 or len(treated_values) < 2:
                    results.append([trip, sample_type, hormone, len(control_values), len(treated_values), "N/A", "N/A", "N/A", "Too few samples", "Manual Review Needed"])
                    continue

                # Perform Mann-Whitney U test
                stat, p_value = mannwhitneyu(control_values, treated_values, alternative='two-sided')

                # Compute Cliff’s Delta effect size
                effect_size, effect_category = cliffs_delta(control_values, treated_values)

                # Interpretation
                if p_value < 0.05:
                    conclusion = "Significant Difference"
                    causation = "Likely Not Random"
                else:
                    conclusion = "No Significant Difference"
                    causation = "Possibly Random or Insufficient Data"

                # Store results
                results.append([
                    trip, sample_type, hormone, len(control_values), len(treated_values),
                    round(p_value, 4), effect_size, effect_category, conclusion, causation
                ])

    # Convert results to DataFrame
    results_df = pd.DataFrame(results, columns=[
        "Trip", "Sample Type", "Hormone", "Control N", "Treated N", "p-value", 
        "Effect Size", "Effect Category", "Conclusion", "Causation"
    ])
    
    # Display results
    print("\nMann-Whitney U Test Results (Consolidated):")
    print(results_df.to_string(index=False))

    return results_df

# Run analysis and get consolidated results
final_results = perform_statistical_analysis(df)

# Save results to CSV for further analysis
final_results.to_csv("Statistics/Non-Parameteric_Analysis_Results.csv", index=False)

# Load the statistical results
results_df = pd.read_csv("Statistics/Non-Parameteric_Analysis_Results.csv")

# Function to analyze statistical significance
def interpret_results(results_df):
    # Identify sample types and hormones with significant differences
    summary = []
    
    for hormone in results_df["Hormone"].unique():
        for sample_type in results_df["Sample Type"].unique():
            subset = results_df[(results_df["Hormone"] == hormone) & (results_df["Sample Type"] == sample_type)]
            
            significant_count = (subset["Conclusion"] == "Significant Difference").sum()
            total_tests = len(subset)
            significance_ratio = significant_count / total_tests if total_tests > 0 else 0

            # Determine if hormone treatment is a primary factor
            if significance_ratio > 0.5:  # More than 50% of trips show significant difference
                conclusion = "Hormone treatment likely caused changes."
            elif significance_ratio > 0:
                conclusion = "Some effect observed, but not consistent."
            else:
                conclusion = "No statistical evidence of hormone impact."

            summary.append([hormone, sample_type, significant_count, total_tests, round(significance_ratio, 2), conclusion])

    summary_df = pd.DataFrame(summary, columns=["Hormone", "Sample Type", "Significant Tests", "Total Tests", "Significance Ratio", "Conclusion"])
    
    # Save in proper CSV format
    summary_df.to_csv("Statistics/Hormone_Analysis_Summary.csv", index=False)

    return summary_df

# Run interpretation and store results
summary_df = interpret_results(results_df)
