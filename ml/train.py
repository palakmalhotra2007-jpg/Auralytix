import os
import sys
import argparse
import json
from pathlib import Path
from datetime import datetime

import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.svm import SVC
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    classification_report,
    confusion_matrix,
)

# Resolve paths relative to project root
BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_DATA_PATH = BASE_DIR / "data" / "WA_Fn-UseC_-Telco-Customer-Churn.csv"
DEFAULT_MODEL_DIR = Path(__file__).resolve().parent / "saved_model"

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

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
    """Loads Telco dataset, cleans TotalCharges, drops customer ID, and encodes target."""
    if not os.path.exists(data_path):
        raise FileNotFoundError(
            f"Dataset not found at: {data_path}. "
            f"Please verify 'WA_Fn-UseC_-Telco-Customer-Churn.csv' exists in '{data_path.parent}'."
        )

    df = pd.read_csv(data_path)

    # Coerce TotalCharges to numeric (handles whitespace strings for zero-tenure accounts)
    if "TotalCharges" in df.columns:
        df["TotalCharges"] = pd.to_numeric(
            df["TotalCharges"].astype(str).str.strip(), errors="coerce"
        ).fillna(0.0)

    # Drop identifier column
    if "customerID" in df.columns:
        df = df.drop(columns=["customerID"])

    if TARGET_COLUMN not in df.columns:
        raise ValueError(
            f"Target column '{TARGET_COLUMN}' not found in columns: {list(df.columns)}"
        )

    # Encode target: Yes -> 1, No -> 0
    y = df[TARGET_COLUMN].astype(str).str.strip().map({"Yes": 1, "No": 0})
    if y.isna().any():
        y = df[TARGET_COLUMN].astype(int)

    X = df.drop(columns=[TARGET_COLUMN])
    return X, y


def build_preprocessor():
    """Builds scikit-learn ColumnTransformer for numerical and categorical features."""
    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(drop="first", handle_unknown="ignore")),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, NUMERIC_FEATURES),
            ("cat", categorical_transformer, CATEGORICAL_FEATURES),
        ]
    )
    return preprocessor


def train_and_evaluate(
    data_path: Path = DEFAULT_DATA_PATH,
    model_dir: Path = DEFAULT_MODEL_DIR,
):
    print("=" * 60)
    print("      Auralytix Support Vector Machine (SVM) Training Pipeline      ")
    print("=" * 60)
    print(f"[Auralytix ML] Loading raw dataset: {data_path}")
    X, y = load_and_preprocess_raw_data(data_path)
    print(f"[Auralytix ML] Dataset loaded: {X.shape[0]} samples, {X.shape[1]} features.")
    print(f"[Auralytix ML] Class distribution: Retained={sum(y==0)}, Churned={sum(y==1)} ({sum(y==1)/len(y)*100:.1f}%)")

    # Stratified 80/20 train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    preprocessor = build_preprocessor()

    # SVM Pipeline with balanced class weights for optimal churn recall
    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            (
                "classifier",
                SVC(
                    kernel="rbf",
                    probability=True,
                    class_weight="balanced",
                    C=1.0,
                    gamma="scale",
                    random_state=42,
                    cache_size=500,
                ),
            ),
        ]
    )

    print("[Auralytix ML] Fitting SVM RBF Classifier pipeline on training data...")
    pipeline.fit(X_train, y_train)

    # Evaluate on held-out test set
    y_pred = pipeline.predict(X_test)
    y_prob = pipeline.predict_proba(X_test)[:, 1]

    accuracy = float(accuracy_score(y_test, y_pred))
    precision = float(precision_score(y_test, y_pred, zero_division=0))
    recall = float(recall_score(y_test, y_pred, zero_division=0))
    f1 = float(f1_score(y_test, y_pred, zero_division=0))
    roc_auc = float(roc_auc_score(y_test, y_prob))
    conf_mat = confusion_matrix(y_test, y_pred).tolist()

    print("\n" + "=" * 60)
    print("         Auralytix SVM Model Evaluation Results")
    print("=" * 60)
    print(f"  Accuracy Score:   {accuracy:.4f}  ({accuracy*100:.2f}%)")
    print(f"  ROC-AUC Score:    {roc_auc:.4f}")
    print(f"  Precision:        {precision:.4f}")
    print(f"  Recall:           {recall:.4f}")
    print(f"  F1-Score:         {f1:.4f}")
    print("=" * 60)
    print("\nDetailed Classification Report:")
    print(classification_report(y_test, y_pred, target_names=["Retained (0)", "Churned (1)"], zero_division=0))
    print("Confusion Matrix [[TN, FP], [FN, TP]]:", conf_mat)

    # Save trained pipeline and background dataset for explainability
    os.makedirs(model_dir, exist_ok=True)
    model_path = model_dir / "churn_pipeline.joblib"
    joblib.dump(pipeline, model_path)
    print(f"[Auralytix ML] Model pipeline saved -> {model_path}")

    # Background samples for SHAP
    bg_sample = X_train.sample(n=min(100, len(X_train)), random_state=42)
    bg_path = model_dir / "background_samples.joblib"
    joblib.dump(bg_sample, bg_path)
    print(f"[Auralytix ML] Saved SHAP background samples -> {bg_path}")

    # Save model metadata
    metadata = {
        "model_type": "SupportVectorMachine (SVC RBF)",
        "model_version": "svm_rbf_v2.0",
        "trained_timestamp": datetime.now().isoformat(),
        "target": TARGET_COLUMN,
        "dataset_rows": len(X),
        "test_rows": len(X_test),
        "metrics": {
            "accuracy": round(accuracy, 4),
            "roc_auc": round(roc_auc, 4),
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1_score": round(f1, 4),
            "confusion_matrix": conf_mat,
        },
        "features": {
            "numeric": NUMERIC_FEATURES,
            "categorical": CATEGORICAL_FEATURES,
        },
    }

    metadata_path = model_dir / "model_metadata.json"
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
    print(f"[Auralytix ML] Model metadata saved -> {metadata_path}")

    # Sync to AWS S3 if configured
    try:
        from backend.cloud.s3_service import upload_model_artifacts
        print("[Auralytix ML] Checking AWS S3 sync...")
        upload_results = upload_model_artifacts(model_dir)
        print(f"[Auralytix ML] S3 Artifact sync status: {upload_results}")
    except Exception as e:
        print(f"[Auralytix ML] Note: AWS S3 sync skipped or not configured: {e}")

    return pipeline, metadata


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train Auralytix Telco Churn SVM RBF Pipeline")
    parser.add_argument("--data-path", type=str, default=str(DEFAULT_DATA_PATH), help="Path to input CSV")
    parser.add_argument("--model-dir", type=str, default=str(DEFAULT_MODEL_DIR), help="Output directory for saved model")
    args = parser.parse_args()

    train_and_evaluate(data_path=Path(args.data_path), model_dir=Path(args.model_dir))
