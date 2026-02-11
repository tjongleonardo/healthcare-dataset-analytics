import pandas as pd
from pathlib import Path

# ---------- Load Data ----------
BASE_DIR = Path(__file__).resolve().parent.parent
csv_path = BASE_DIR / "Data" / "healthcare_dataset.csv"

df = pd.read_csv(csv_path)

df["Date of Admission"] = pd.to_datetime(df["Date of Admission"])
df["Discharge Date"] = pd.to_datetime(df["Discharge Date"])

df["Length_of_Stay"] = (
    df["Discharge Date"] - df["Date of Admission"]
).dt.days

df["Cost_per_Day"] = df["Billing Amount"] / df["Length_of_Stay"]

# ---------- Summary Statistics ----------
avg_los = round(df["Length_of_Stay"].mean(), 2)
max_los = df["Length_of_Stay"].max()
min_los = df["Length_of_Stay"].min()

avg_cost = df["Billing Amount"].mean()
avg_cost_per_day = df["Cost_per_Day"].mean()

print("\n=== Length of Stay Summary ===")
print(f"Average Length of Stay: {avg_los:.2f} days")
print(f"Maximum Length of Stay: {max_los} {'day' if max_los == 1 else 'days'}")
print(f"Minimum Length of Stay: {min_los} {'day' if min_los == 1 else 'days'}")

print("\n=== Financial Summary ===")
print(f"Average Billing per Patient: ${avg_cost:,.2f}")
print(f"Average Cost per Day: ${avg_cost_per_day:,.2f}")

# ---------- Top Conditions by Daily Cost ----------
print("\n=== Top 5 Conditions by Average Cost per Day ===")

top_cost = (
    df.groupby("Medical Condition")["Cost_per_Day"]
      .mean()
      .sort_values(ascending=False)
      .head()
)

for condition, value in top_cost.items():
    print(f"{condition}: ${value:,.2f} per day")

# ---------- Insurance Distribution ----------
print("\n=== Insurance Distribution ===")

counts = df["Insurance Provider"].value_counts()
percent = df["Insurance Provider"].value_counts(normalize=True) * 100

for provider in counts.index:
    print(f"{provider}: {counts[provider]:,} patients ({percent[provider]:.2f}%)")

# ---------- Display Columns ----------
df["Length of Stay"] = df["Length_of_Stay"].apply(
    lambda x: f"{x} day" if x == 1 else f"{x} days"
)

df["Cleaned Bill"] = df["Billing Amount"].apply(
    lambda x: f"${x:,.2f}"
)

df["Cost Per Day"] = df["Cost_per_Day"].apply(
    lambda x: f"${x:,.2f} per day"
)

# -------- Formatting Improvements --------
# Clean name capitalization
df["Name"] = df["Name"].str.title()

# Custom sort for Admission Type
admission_order = ["Emergency", "Urgent", "Elective"]

df["Admission Type"] = pd.Categorical(
    df["Admission Type"],
    categories=admission_order,
    ordered=True
)

df = df.sort_values(by=["Admission Type", "Date of Admission"])


# -------- Save Processed Dataset --------
output_path = BASE_DIR / "Outputs" / "healthcare_clean.csv"

df_export = df.drop(columns=["Length of Stay", "Cleaned Bill", "Cost Per Day"])
df_export.to_csv(output_path, index=False)

print("\nSaved cleaned dataset.")


