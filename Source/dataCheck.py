import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
csv_path = BASE_DIR / "Data" / "healthcare_dataset.csv"

print("Looking for file at:", csv_path)

df = pd.read_csv(csv_path)

print("Rows, Columns:", df.shape)
print(df.head(5))
print("\nColumns:\n", df.columns)
print("\nMissing values:\n", df.isna().sum())
