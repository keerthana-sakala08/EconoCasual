from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from io import BytesIO

app = Flask(__name__)
CORS(app)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB upload limit

@app.get("/api/health")
def health():
    return jsonify({"status": "ok", "service": "EconoCausal API"})

@app.post("/api/analyze")
def analyze_csv():
    uploaded = request.files.get("file")
    if uploaded is None or uploaded.filename == "":
        return jsonify({"error": "Please choose a CSV file."}), 400
    if not uploaded.filename.lower().endswith(".csv"):
        return jsonify({"error": "Only CSV files are supported in this version."}), 400
    try:
        df = pd.read_csv(BytesIO(uploaded.read()))
        if df.empty:
            return jsonify({"error": "The CSV file has no data rows."}), 400

        columns = []
        for name in df.columns:
            columns.append({
                "name": str(name),
                "dtype": str(df[name].dtype),
                "missing": int(df[name].isna().sum())
            })

        numeric = df.select_dtypes(include="number")
        numeric_summary = {}
        for name in numeric.columns:
            series = numeric[name].dropna()
            numeric_summary[str(name)] = {
                "mean": round(float(series.mean()), 4) if not series.empty else 0,
                "min": round(float(series.min()), 4) if not series.empty else 0,
                "max": round(float(series.max()), 4) if not series.empty else 0,
                "std": round(float(series.std()), 4) if len(series) > 1 else 0
            }

        return jsonify({
            "filename": uploaded.filename,
            "rows": int(len(df)),
            "columns": columns,
            "numeric_summary": numeric_summary
        })
    except pd.errors.EmptyDataError:
        return jsonify({"error": "The CSV file is empty."}), 400
    except Exception as exc:
        return jsonify({"error": f"Could not read CSV: {str(exc)}"}), 400

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
