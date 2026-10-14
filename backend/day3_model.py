<<<<<<< HEAD

import pandas as pd
from pathlib import Path
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

# Find the project dataset
project_dir = Path(__file__).resolve().parent.parent
clean_file = project_dir / "sample_data" / "cleaned_sales_data.csv"
raw_file = project_dir / "sample_data" / "sales_data.csv"

data_file = clean_file if clean_file.exists() else raw_file

if not data_file.exists():
    raise FileNotFoundError(
        "Dataset not found. Run data_analysis.py first."
    )

# Load the data
df = pd.read_csv(data_file)

# Check required columns
required = ["discount", "advertising", "sales"]
missing = [col for col in required if col not in df.columns]

if missing:
    raise ValueError(f"Missing required columns: {missing}")

# Keep relevant columns and clean missing values
df = df[required].apply(pd.to_numeric, errors="coerce")
df = df.dropna()

if len(df) < 3:
    raise ValueError("At least 3 valid rows are needed for this demo.")

# Features: discount and advertising
X = df[["discount", "advertising"]]

# Target: sales
y = df["sales"]

# Train a simple baseline regression model
model = LinearRegression()
model.fit(X, y)

# Predict sales on the same data for a basic demonstration
predictions = model.predict(X)

print("\n===== ECONOCAUSAL DAY 3 =====")
print("Rows used:", len(df))
print("\nModel: Linear Regression")
print("Features: discount, advertising")
print("Target: sales")

print("\nModel coefficients:")
for feature, coefficient in zip(X.columns, model.coef_):
    print(f"{feature}: {coefficient:.3f}")

print(f"\nIntercept: {model.intercept_:.3f}")
print(f"Mean Absolute Error: {mean_absolute_error(y, predictions):.3f}")
print(f"R-squared (in-sample): {r2_score(y, predictions):.3f}")

print("\nExample predictions:")
results = df.copy()
results["predicted_sales"] = predictions.round(2)
print(results.head())

print("\nDay 3 baseline model completed!")
print("Note: This is a demonstration, not a causal estimate.")
=======

import pandas as pd
from pathlib import Path
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

# Find the project dataset
project_dir = Path(__file__).resolve().parent.parent
clean_file = project_dir / "sample_data" / "cleaned_sales_data.csv"
raw_file = project_dir / "sample_data" / "sales_data.csv"

data_file = clean_file if clean_file.exists() else raw_file

if not data_file.exists():
    raise FileNotFoundError(
        "Dataset not found. Run data_analysis.py first."
    )

# Load the data
df = pd.read_csv(data_file)

# Check required columns
required = ["discount", "advertising", "sales"]
missing = [col for col in required if col not in df.columns]

if missing:
    raise ValueError(f"Missing required columns: {missing}")

# Keep relevant columns and clean missing values
df = df[required].apply(pd.to_numeric, errors="coerce")
df = df.dropna()

if len(df) < 3:
    raise ValueError("At least 3 valid rows are needed for this demo.")

# Features: discount and advertising
X = df[["discount", "advertising"]]

# Target: sales
y = df["sales"]

# Train a simple baseline regression model
model = LinearRegression()
model.fit(X, y)

# Predict sales on the same data for a basic demonstration
predictions = model.predict(X)

print("\n===== ECONOCAUSAL DAY 3 =====")
print("Rows used:", len(df))
print("\nModel: Linear Regression")
print("Features: discount, advertising")
print("Target: sales")

print("\nModel coefficients:")
for feature, coefficient in zip(X.columns, model.coef_):
    print(f"{feature}: {coefficient:.3f}")

print(f"\nIntercept: {model.intercept_:.3f}")
print(f"Mean Absolute Error: {mean_absolute_error(y, predictions):.3f}")
print(f"R-squared (in-sample): {r2_score(y, predictions):.3f}")

print("\nExample predictions:")
results = df.copy()
results["predicted_sales"] = predictions.round(2)
print(results.head())

print("\nDay 3 baseline model completed!")
print("Note: This is a demonstration, not a causal estimate.")
>>>>>>> 07448fdae668d93133004a57602a04b45c057272
