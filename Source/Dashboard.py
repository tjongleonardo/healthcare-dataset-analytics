import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# ---------- Load ----------
BASE_DIR = Path(__file__).resolve().parent.parent
df = pd.read_csv(BASE_DIR / "Outputs" / "healthcare_clean.csv")

# ---------- Feature Engineering ----------
df["Age Group"] = pd.cut(
    df["Age"],
    bins=[0, 18, 35, 50, 65, 100],
    labels=["0-18", "19-35", "36-50", "51-65", "65+"]
)

# High cost threshold (top 10%)
threshold = df["Cost_per_Day"].quantile(0.90)
df["High Cost Case"] = df["Cost_per_Day"] > threshold

# ---------- KPIs (Key Performance Indicator)----------
total_patients = len(df)
avg_billing = df["Billing Amount"].mean()
avg_los = df["Length_of_Stay"].mean()
correlation = df["Length_of_Stay"].corr(df["Billing Amount"])
high_cost_pct = df["High Cost Case"].mean() * 100

# ---------- Aggregations ----------
# Pareto billing by condition
billing_by_condition = (
    df.groupby("Medical Condition")["Billing Amount"]
      .sum()
      .sort_values(ascending=False)
)

cumulative_pct = billing_by_condition.cumsum() / billing_by_condition.sum() * 100

# Age group billing
age_billing = df.groupby("Age Group")["Billing Amount"].mean()

# Admission type ordering
admission_order = ["Emergency", "Urgent", "Elective"]
groups = [df[df["Admission Type"] == t]["Billing Amount"] for t in admission_order]

# ---------- Dashboard ----------
fig, axes = plt.subplots(2, 2, figsize=(16, 10))

fig.suptitle(
    f"Healthcare Operations Analytics Dashboard\n"
    f"Patients: {total_patients:,} | "
    f"Avg Billing: ${avg_billing:,.0f} | "
    f"Avg LoS: {avg_los:.1f} days | "
    f"LoS-Billing Corr: {correlation:.2f} | "
    f"Top 10% High-Cost Cases: {high_cost_pct:.1f}%",
    fontsize=13
)

# 1️ Scatter + Trendline
axes[0, 0].scatter(df["Length_of_Stay"], df["Billing Amount"], s=8, alpha=0.15)

z = np.polyfit(df["Length_of_Stay"], df["Billing Amount"], 1)
p = np.poly1d(z)
axes[0, 0].plot(df["Length_of_Stay"], p(df["Length_of_Stay"]))

axes[0, 0].set_title("Billing vs Length of Stay")
axes[0, 0].set_xlabel("Length of Stay (Days)")
axes[0, 0].set_ylabel("Billing Amount")

# 2️ Pareto Chart
axes[0, 1].bar(billing_by_condition.index, billing_by_condition.values)
axes[0, 1].set_title("Total Billing by Condition")
axes[0, 1].tick_params(axis="x", rotation=45)

ax2 = axes[0, 1].twinx()
ax2.plot(billing_by_condition.index, cumulative_pct, marker="o")
ax2.set_ylabel("Cumulative %")
ax2.set_ylim(0, 110)

# 3️ Boxplot by Admission Type
axes[1, 0].boxplot(groups, labels=admission_order, showfliers=False)
axes[1, 0].set_title("Billing Distribution by Admission Type")
axes[1, 0].set_xlabel("Admission Type")
axes[1, 0].set_ylabel("Billing Amount")

# 4️ Average Billing by Age Group
axes[1, 1].bar(age_billing.index.astype(str), age_billing.values)
axes[1, 1].set_title("Average Billing by Age Group")
axes[1, 1].set_xlabel("Age Group")
axes[1, 1].set_ylabel("Average Billing")

plt.tight_layout(rect=[0, 0.03, 1, 0.93])

# ---------- Save ----------
charts_dir = BASE_DIR / "Outputs"
charts_dir.mkdir(parents=True, exist_ok=True)
output_path = charts_dir / "healthcare_dashboard.png"

plt.savefig(output_path, dpi=300)
plt.show()

print(f"Dashboard saved to: {output_path}")
