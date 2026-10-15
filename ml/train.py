import os
import sys
import argparse
import json
from pathlib import Path

import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    accuracy_score,
    classification_report,
)

# Resolve paths relative to project root
BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_DATA_PATH = BASE_DIR / "data" / "WA_Fn-UseC_-Telco-Customer-Churn.csv"
DEFAULT_MODEL_DIR = Path(__file__).resolve().parent / "saved_model"

NUMERIC_FEATURES = ["tenure", "MonthlyCharges", "TotalCharges"]
CATEGORICAL_FEATURES = [
    "gender",
    "SeniorCitizen",
    "Partner",
    "Dependents",
    "PhoneService",
    "MultipleLines",
    "InternetService",
    "OnlineSecurity",
    "OnlineBackup",
    "DeviceProtection",
    "TechSupport",
    "StreamingTV",
    "StreamingMovies",
    "Contract",
    "PaperlessBilling",
    "PaymentMethod",
]
TARGET_COLUMN = "Churn"


def load_and_preprocess_raw_data(data_path: Path):
    if not os.path.exists(data_path):
        raise FileNotFoundError(
            f"Dataset not found at: {data_path}. "
            f"Please place 'WA_Fn-UseC_-Telco-Customer-Churn.csv' into the '{data_path.parent}' folder."
        )

    df = pd.read_csv(data_path)

    # Coerce TotalCharges to numeric (handles blank spaces for new accounts)
    if "TotalCharges" in df.columns:
        df["TotalCharges"] = pd.to_numeric(df["TotalCharges"].astype(str).str.strip(), errors="coerce")
        df["TotalCharges"] = df["TotalCharges"].fillna(0.0)

    # Drop identifier column if present
    if "customerID" in df.columns:
        df = df.drop(columns=["customerID"])

    # Ensure target column exists
    if TARGET_COLUMN not in df.columns:
        raise ValueError(f"Target column '{TARGET_COLUMN}' not found in dataset columns: {list(df.columns)}")

    # Encode target: Yes -> 1, No -> 0
    y = df[TARGET_COLUMN].astype(str).str.strip().map({"Yes": 1, "No": 0})
    if y.isna().any():
        y = df[TARGET_COLUMN].astype(int)

    X = df.drop(columns=[TARGET_COLUMN])
    return X, y


def build_pipeline():
    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, NUMERIC_FEATURES),
            ("cat", categorical_transformer, CATEGORICAL_FEATURES),
        ]
    )

    model_pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", LogisticRegression(max_iter=1000, random_state=42, class_weight="balanced")),
        ]
    )

    return model_pipeline


def train_and_evaluate(data_path: Path = DEFAULT_DATA_PATH, model_dir: Path = DEFAULT_MODEL_DIR):
    print(f"[Auralytix ML] Loading dataset from: {data_path}")
    X, y = load_and_preprocess_raw_data(data_path)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    pipeline = build_pipeline()

    print("[Auralytix ML] Training Logistic Regression model pipeline...")
    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    y_prob = pipeline.predict_proba(X_test)[:, 1]

    precision = precision_score(y_test, y_pred, zero_division=0)
    recall = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    roc_auc = roc_auc_score(y_test, y_prob)
    accuracy = accuracy_score(y_test, y_pred)

    print("\n" + "=" * 50)
    print("      Auralytix Churn Model Evaluation Results      ")
    print("=" * 50)
    print(f"Accuracy:         {accuracy:.4f}")
    print(f"Precision:        {precision:.4f}")
    print(f"Recall:           {recall:.4f}")
    print(f"F1-Score:         {f1:.4f}")
    print(f"ROC-AUC:          {roc_auc:.4f}")
    print("=" * 50)
    print("\nClassification Report:\n", classification_report(y_test, y_pred, zero_division=0))

    # Save pipeline and metadata
    os.makedirs(model_dir, exist_ok=True)
    model_path = model_dir / "churn_pipeline.joblib"
    joblib.dump(pipeline, model_path)
    print(f"[Auralytix ML] Saved pipeline to: {model_path}")

    metadata = {
        "model_type": "LogisticRegression",
        "target": TARGET_COLUMN,
        "numeric_features": NUMERIC_FEATURES,
        "categorical_features": CATEGORICAL_FEATURES,
        "metrics": {
            "accuracy": round(float(accuracy), 4),
            "precision": round(float(precision), 4),
            "recall": round(float(recall), 4),
            "f1_score": round(float(f1), 4),
            "roc_auc": round(float(roc_auc), 4),
        },
    }

    metadata_path = model_dir / "model_metadata.json"
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
    print(f"[Auralytix ML] Saved model metadata to: {metadata_path}")

    return pipeline, metadata


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train Auralytix Telco Churn Logistic Regression Pipeline")
    parser.add_argument("--data-path", type=str, default=str(DEFAULT_DATA_PATH), help="Path to input CSV")
    parser.add_argument("--model-dir", type=str, default=str(DEFAULT_MODEL_DIR), help="Output directory for saved model")
    args = parser.parse_args()

    train_and_evaluate(data_path=Path(args.data_path), model_dir=Path(args.model_dir))
