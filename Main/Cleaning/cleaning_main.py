import pandas as pd

# Load dataset with correct delimiter and skip first row (metadata)
df = pd.read_csv("Statistics\DatasetBio.csv", delimiter=";", skiprows=1)

# Rename columns correctly
df.columns = ["Sample_Number", "Sample_Name"] + df.columns[2:].tolist()
# Convert hormone data to numeric, replacing commas and handling missing values
for col in df.columns[2:]:
    df[col] = pd.to_numeric(df[col].astype(str).str.replace(",", "."), errors="coerce")

df["Control"] = df["Sample_Name"].str.strip().str[0] == "K"
df["Hormone_Treated"] = df["Sample_Name"].str.contains(r"\bGA[1-4]\b", regex=True)
trip_map = {"A": 1, "B": 2, "C": 3, "D": 4}
df["Trip_Number"] = df["Sample_Name"].str.strip().str[-1].map(trip_map)
df.to_csv("Statistics/Cleaned_DatasetBio.csv", index=False, sep=";")
