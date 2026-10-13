
import pandas as pd
import numpy as np
from pathlib import Path

# Project dataset location
DATA_FILE = (
    Path(__file__).resolve().parent.parent
    / "sample_data"
    / "sales_data.csv"
)

# Create sample data if the CSV does not exist yet
if not DATA_FILE.exists():
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

    df_sample = pd.DataFrame({
        "price": [100, 90, 80, 100, 85, 95, 75, 90],
        "discount": [0, 10, 20, 0, 15, 5, 25, 10],
        "advertising": [5, 7, 8, 4, 6, 5, 9, 7],
        "sales": [20, 25, 32, 18, 28, 22, 38, 27]
    })

    df_sample.to_csv(DATA_FILE, index=False)

# Load the dataset
df = pd.read_csv(DATA_FILE)

print("\n===== ECONOCAUSAL: DAY 2 =====")
print("\n1. First five rows:")
print(df.head())

print("\n2. Dataset shape:")
print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")

print("\n3. Column data types:")
print(df.dtypes)

print("\n4. Missing values:")
print(df.isnull().sum())

# Remove duplicate records
df = df.drop_duplicates().copy()

# Fill missing numeric values with their column median
numeric_cols = df.select_dtypes(include=np.number).columns
df[numeric_cols] = df[numeric_cols].fillna(
    df[numeric_cols].median()
)

# Basic statistics
print("\n5. Descriptive statistics:")
print(df.describe().round(2))

print("\n6. Average sales:")
print(round(df["sales"].mean(), 2))

print("\n7. Average discount:")
print(round(df["discount"].mean(), 2))

print("\n8. Correlation with sales:")
print(df.corr(numeric_only=True)["sales"].round(2))

# Save the cleaned dataset
clean_file = DATA_FILE.parent / "cleaned_sales_data.csv"
df.to_csv(clean_file, index=False)

print(f"\nCleaned dataset saved to: {clean_file}")
print("\n Analysis completed successfully!")
