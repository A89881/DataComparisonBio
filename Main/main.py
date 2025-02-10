import pandas as pd
df = pd.read_csv("DatasetBio.csv", delimiter=";", skiprows=1)

for col in df.columns[2:]:
    df[col] = pd.to_numeric(df[col].astype(str).str.replace(",", "."), errors="coerce")

df["Control"] = df["Sample_Name"].str.startswith("K")
df["Hormone_Treated"] = df["Sample_Name"].str.contains(r"GA[1-4]", regex=True)
trip_map = {"A": 1, "B": 2, "C": 3, "D": 4}
df["Trip_Number"] = df["Sample_Name"].str.strip().str[-1].map(trip_map)
df.to_csv("Cleaned_DatasetBio.csv", index=False, sep=";")
