
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import KFold

# ==========================================
# ECONOCAUSAL - DAY 4
# Double Machine Learning (DML) Demonstration
# ==========================================

# Find project dataset
project_dir = Path(__file__).resolve().parent.parent

clean_file = project_dir / "sample_data" / "cleaned_sales_data.csv"
raw_file = project_dir / "sample_data" / "sales_data.csv"

data_file = clean_file if clean_file.exists() else raw_file

if not data_file.exists():
    raise FileNotFoundError(
        "Dataset not found. Add sales_data.csv to sample_data."
    )

# Load data
df = pd.read_csv(data_file)

# Required columns
required = ["discount", "advertising", "sales"]
missing = [col for col in required if col not in df.columns]

if missing:
    raise ValueError(f"Missing required columns: {missing}")

# Clean numeric values
df = df[required].apply(pd.to_numeric, errors="coerce")
df = df.replace([np.inf, -np.inf], np.nan).dropna()

if len(df) < 6:
    raise ValueError(
        "At least 6 valid rows are needed for this demonstration. "
        "More data is strongly recommended."
    )

if df["discount"].nunique() < 2:
    raise ValueError("Discount must have at least two different values.")

# Treatment: discount
treatment = df["discount"].to_numpy(dtype=float)

# Outcome: sales
outcome = df["sales"].to_numpy(dtype=float)

# Control variables: advertising
controls = df[["advertising"]].to_numpy(dtype=float)

# Cross-fitting
n_splits = min(5, len(df))
cv = KFold(n_splits=n_splits, shuffle=True, random_state=42)

# Store out-of-fold predictions
predicted_treatment = np.zeros(len(df))
predicted_outcome = np.zeros(len(df))

for train_idx, test_idx in cv.split(controls):
    # Predict discount using control variables
    treatment_model = RandomForestRegressor(
        n_estimators=100,
        min_samples_leaf=2,
        random_state=42
    )
    treatment_model.fit(controls[train_idx], treatment[train_idx])
    predicted_treatment[test_idx] = treatment_model.predict(
        controls[test_idx]
    )

    # Predict sales using control variables
    outcome_model = RandomForestRegressor(
        n_estimators=100,
        min_samples_leaf=2,
        random_state=42
    )
    outcome_model.fit(controls[train_idx], outcome[train_idx])
    predicted_outcome[test_idx] = outcome_model.predict(
        controls[test_idx]
    )

# Residualize treatment and outcome
treatment_residual = treatment - predicted_treatment
outcome_residual = outcome - predicted_outcome

# Estimate the partialling-out DML effect
denominator = np.sum(treatment_residual ** 2)

if denominator < 1e-10:
    raise ValueError(
        "Discount variation after controlling for advertising is too small."
    )

causal_effect = (
    np.sum(treatment_residual * outcome_residual) / denominator
)

# Display results
print("\n===== ECONOCAUSAL DAY 4: DML =====")
print("Rows used:", len(df))
print("Treatment: discount")
print("Outcome: sales")
print("Control variable: advertising")
print("Method: Cross-fitted partialling-out DML")

print(f"\nEstimated discount effect: {causal_effect:.4f}")
print(
    "Interpretation: Estimated change in sales for a "
    "one-unit increase in discount, holding the modeled "
    "advertising relationship into account."
)

print("\nImportant limitations:")
print("- This is a demonstration, not proof of causality.")
print("- Reliable causal interpretation requires sufficient data,")
print("  relevant confounders, and appropriate modeling assumptions.")
print("- Small datasets can produce highly unstable estimates.")

print("\nDay 4 DML demonstration completed!")
