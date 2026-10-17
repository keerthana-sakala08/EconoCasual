
from pathlib import Path

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "sample_data" / "cleaned_sales_data.csv"
OUTPUT_DIR = BASE_DIR / "outputs"

st.set_page_config(
    page_title="EconoCausal Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("EconoCausal: Dynamic Pricing Dashboard")
st.write("Sales analysis, model evaluation, and discount-effect estimation.")

if not DATA_FILE.exists():
    st.error(f"Dataset not found: {DATA_FILE}")
    st.info("Check that sample_data/cleaned_sales_data.csv exists.")
    st.stop()

df = pd.read_csv(DATA_FILE)

st.header("1. Dataset Overview")
st.write(f"**Total records:** {len(df)}")
st.dataframe(df, use_container_width=True)

if {"sales", "discount"}.issubset(df.columns):
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Average Sales", f"{df['sales'].mean():.2f}")

    with col2:
        st.metric("Average Discount", f"{df['discount'].mean():.2f}")

    with col3:
        st.metric("Total Sales", f"{df['sales'].sum():.2f}")

st.header("2. Model Evaluation")

metrics_file = OUTPUT_DIR / "day5_metrics.csv"
predictions_file = OUTPUT_DIR / "day5_predictions.csv"

if metrics_file.exists():
    metrics = pd.read_csv(metrics_file)
    st.subheader("Evaluation Metrics")
    st.dataframe(metrics, use_container_width=True)
else:
    st.warning("Run backend/day5_evaluation.py to generate metrics.")

if predictions_file.exists():
    predictions = pd.read_csv(predictions_file)
    st.subheader("Actual vs Predicted Sales")
    st.dataframe(predictions, use_container_width=True)

graph_files = [
    ("Actual vs Predicted Sales", "actual_vs_predicted.png"),
    ("Discount vs Sales", "discount_vs_sales.png"),
]

st.header("3. Visualizations")

for title, filename in graph_files:
    graph_path = OUTPUT_DIR / filename
    if graph_path.exists():
        st.subheader(title)
        st.image(str(graph_path), use_container_width=True)
    else:
        st.info(f"{filename} is not available yet.")

st.header("4. Discount Effect Analysis")

if {"discount", "sales"}.issubset(df.columns):
    correlation = df["discount"].corr(df["sales"])
    st.write(
        f"**Discount-sales correlation:** "
        f"{correlation:.3f}" if pd.notna(correlation)
        else "Correlation could not be calculated."
    )

    st.caption(
        "Correlation is not a causal effect. Refer to the Day 4 "
        "DML estimate separately. Results from a very small dataset "
        "are only a demonstration."
    )

st.success("EconoCausal dashboard loaded successfully.")
