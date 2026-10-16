
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "sample_data"
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

# Load available dataset
cleaned_file = DATA_DIR / "cleaned_sales_data.csv"
sales_file = DATA_DIR / "sales_data.csv"

data_file = cleaned_file if cleaned_file.exists() else sales_file

if not data_file.exists():
    raise FileNotFoundError(
        "Sales data not found. Add sales_data.csv to sample_data."
    )

df = pd.read_csv(data_file)

# Validate and clean required columns
required_columns = ["discount", "advertising", "sales"]

missing_columns = [
    column for column in required_columns if column not in df.columns
]

if missing_columns:
    raise ValueError(f"Missing columns: {missing_columns}")

df = df[required_columns].apply(pd.to_numeric, errors="coerce")
df = df.dropna()

if len(df) < 5:
    raise ValueError("At least 5 valid rows are required for evaluation.")

if df["sales"].nunique() < 2:
    raise ValueError("Sales must contain at least two different values.")

# Select features and target
X = df[["discount", "advertising"]]
y = df["sales"]

# Split data before training
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)

# Train baseline model
model = LinearRegression()
model.fit(X_train, y_train)

# Predict sales for unseen test rows
predictions = model.predict(X_test)

# Evaluate performance
mae = mean_absolute_error(y_test, predictions)
rmse = mean_squared_error(y_test, predictions) ** 0.5
r2 = r2_score(y_test, predictions) if len(y_test) >= 2 else float("nan")

print("\n===== ECONOCAUSAL DAY 5 =====")
print(f"Dataset: {data_file.name}")
print(f"Total valid rows: {len(df)}")
print(f"Training rows: {len(X_train)}")
print(f"Testing rows: {len(X_test)}")
print(f"MAE: {mae:.3f}")
print(f"RMSE: {rmse:.3f}")
print(f"R²: {r2:.3f}")
print("\nNote: A small dataset makes these metrics unreliable.")

# Save actual vs predicted results
results = pd.DataFrame({
    "Actual_Sales": y_test.to_numpy(),
    "Predicted_Sales": predictions
})

results.to_csv(OUTPUT_DIR / "day5_predictions.csv", index=False)

# Graph 1: Actual vs predicted sales
plt.figure(figsize=(7, 5))
plt.scatter(y_test, predictions)
plt.xlabel("Actual Sales")
plt.ylabel("Predicted Sales")
plt.title("Actual vs Predicted Sales")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "actual_vs_predicted.png", dpi=150)
plt.close()

# Graph 2: Discount vs sales
plt.figure(figsize=(7, 5))
plt.scatter(df["discount"], df["sales"])
plt.xlabel("Discount")
plt.ylabel("Sales")
plt.title("Discount vs Sales")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "discount_vs_sales.png", dpi=150)
plt.close()

# Save evaluation metrics
metrics = pd.DataFrame([{
    "MAE": mae,
    "RMSE": rmse,
    "R2": r2,
    "Total_Rows": len(df)
}])

metrics.to_csv(OUTPUT_DIR / "day5_metrics.csv", index=False)

print(f"\nGraphs and reports saved in: {OUTPUT_DIR}")
print("Day 5 evaluation completed successfully!")
