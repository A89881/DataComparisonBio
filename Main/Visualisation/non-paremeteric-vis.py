import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load the summarized statistical results
summary_df = pd.read_csv("Statistics/Hormone_Analysis_Summary.csv")

def visualize_hormone_analysis(summary_df, method="heatmap"):
    if method == "heatmap":
        # Prepare pivot table for heatmap
        heatmap_data = summary_df.pivot(index="Hormone", columns="Sample Type", values="Significance Ratio")

        # Set figure size and create heatmap
        plt.figure(figsize=(12, 8))
        sns.heatmap(heatmap_data, cmap="coolwarm", annot=True, fmt=".2f", linewidths=0.5, cbar_kws={"label": "Significance Ratio"})

        plt.xlabel("Sample Type")
        plt.ylabel("Hormone")
        plt.title("Significance Ratio Heatmap (Hormone-Sample by Trip)")
        plt.xticks(rotation=45)
        plt.yticks(rotation=0)
        
        plt.tight_layout()
        plt.savefig("Statistics/Plots/Hormone_Analysis_Heatmap.png")
        plt.show()

    elif method == "bar":
        plt.figure(figsize=(14, 7))

        # Bar plot with proper spacing
        ax = sns.barplot(
            data=summary_df, 
            x="Sample Type", 
            y="Significance Ratio", 
            hue="Hormone", 
            palette="tab10"
        )

        # Auto-scaling in quarters
        y_max = summary_df["Significance Ratio"].max()
        y_ticks = np.arange(0, y_max + 0.25, 0.25)
        ax.set_yticks(y_ticks)

        # Threshold line
        plt.axhline(y=0.5, color="r", linestyle="--", linewidth=1.5)
        plt.text(len(summary_df["Sample Type"].unique()) - 1, 0.52, "50% Threshold", color="red", fontsize=12)

        # Labels & title
        plt.xlabel("Sample Type")
        plt.ylabel("Significance Ratio")
        plt.title("Hormone Treatment Impact by Sample Type")

        # Legend as a separate panel
        plt.legend(title="Hormone", bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)

        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig("Statistics/Plots/Hormone_Analysis_Barplot.png")
        plt.show()

# Run visualization (choose method: "heatmap" or "bar")
visualize_hormone_analysis(summary_df, method="heatmap")
visualize_hormone_analysis(summary_df, method="bar")
