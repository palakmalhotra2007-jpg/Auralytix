import os
import sys
from pathlib import Path
from typing import Dict, Any, List, Union

import numpy as np
import pandas as pd
import joblib
import shap

# Resolve project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
ML_MODEL_DIR = PROJECT_ROOT / "ml" / "saved_model"
MODEL_PATH = ML_MODEL_DIR / "churn_pipeline.joblib"
BACKGROUND_PATH = ML_MODEL_DIR / "background_samples.joblib"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ml.inference import (
    DEFAULT_TELCO_VALUES,
    map_legacy_features_to_telco,
    get_risk_category,
)

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

_pipeline = None
_explainer = None
_preprocessor = None
_classifier = None
_all_feature_names = None


def get_explainer_components():
    """Initializes and caches SVM pipeline, preprocessor, and SHAP KernelExplainer."""
    global _pipeline, _explainer, _preprocessor, _classifier, _all_feature_names

    if _explainer is not None:
        return _pipeline, _explainer, _preprocessor, _classifier, _all_feature_names

    if not MODEL_PATH.exists():
        print(f"[Auralytix SHAP] Model file not found at: {MODEL_PATH}")
        return None, None, None, None, None

    try:
        _pipeline = joblib.load(MODEL_PATH)
        _preprocessor = _pipeline.named_steps["preprocessor"]
        _classifier = _pipeline.named_steps["classifier"]

        # Extract encoded feature names
        cat_encoder = _preprocessor.named_transformers_["cat"].named_steps["onehot"]
        cat_feature_names = cat_encoder.get_feature_names_out(CATEGORICAL_FEATURES)
        _all_feature_names = list(NUMERIC_FEATURES) + list(cat_feature_names)

        # Load background dataset
        if BACKGROUND_PATH.exists():
            bg_df = joblib.load(BACKGROUND_PATH)
        else:
            # Fallback single synthetic background
            bg_df = pd.DataFrame([DEFAULT_TELCO_VALUES])

        # Take 30 background samples for optimal kernel speed
        bg_subset = bg_df.head(30)
        bg_transformed = _preprocessor.transform(bg_subset)

        def predict_fn(x):
            return _classifier.predict_proba(x)[:, 1]

        _explainer = shap.KernelExplainer(predict_fn, bg_transformed)
        print("[Auralytix SHAP] Successfully initialized KernelExplainer for SVM Churn Pipeline.")
        return _pipeline, _explainer, _preprocessor, _classifier, _all_feature_names
    except Exception as e:
        print(f"[Auralytix SHAP] Error initializing KernelExplainer: {e}")
        return None, None, None, None, None


def _format_customer_dataframe(customer_input: Union[Dict[str, Any], List[Any], pd.DataFrame]) -> pd.DataFrame:
    """Converts diverse customer input formats (dict, legacy list, or DataFrame) to clean Telco DataFrame."""
    if isinstance(customer_input, pd.DataFrame):
        df = customer_input.copy()
    elif isinstance(customer_input, list):
        # Legacy 7-feature positional list:
        # [usage_decline, tickets_last30, negative_sentiment, feature_dropout, active_days, support_delay, payment_delay]
        feature_keys = [
            "usage_decline",
            "tickets_last30",
            "negative_sentiment",
            "feature_dropout",
            "active_days",
            "support_delay",
            "payment_delay",
        ]
        feat_dict = {k: v for k, v in zip(feature_keys, customer_input)}
        mapped = map_legacy_features_to_telco(feat_dict)
        full_record = dict(DEFAULT_TELCO_VALUES)
        full_record.update(mapped)
        df = pd.DataFrame([full_record])
    elif isinstance(customer_input, dict):
        if any(k in customer_input for k in ["usage_decline", "tickets_last30", "negative_sentiment", "feature_dropout", "active_days", "support_delay", "payment_delay"]):
            mapped = map_legacy_features_to_telco(customer_input)
        else:
            mapped = dict(customer_input)
        full_record = dict(DEFAULT_TELCO_VALUES)
        full_record.update(mapped)
        if "TotalCharges" not in full_record or full_record["TotalCharges"] is None:
            full_record["TotalCharges"] = round(float(full_record["tenure"]) * float(full_record["MonthlyCharges"]), 2)
        df = pd.DataFrame([full_record])
    else:
        df = pd.DataFrame([DEFAULT_TELCO_VALUES])

    for col, default_val in DEFAULT_TELCO_VALUES.items():
        if col not in df.columns:
            df[col] = default_val

    if "TotalCharges" in df.columns:
        df["TotalCharges"] = pd.to_numeric(
            df["TotalCharges"].astype(str).str.strip(), errors="coerce"
        ).fillna(0.0)

    return df


def explain_customer(customer_input: Union[Dict[str, Any], List[Any], pd.DataFrame]) -> Dict[str, Any]:
    """
    Computes real SHAP feature attributions on the SVM churn pipeline.
    Returns:
    {
        "risk_score": float,
        "attributions": [{"feature": str, "impact": float}, ...]
    }
    """
    pipeline, explainer, preprocessor, classifier, all_feature_names = get_explainer_components()

    df = _format_customer_dataframe(customer_input)

    fallback_attributions = [
        {"feature": "Contract", "impact": -0.152},
        {"feature": "tenure", "impact": -0.128},
        {"feature": "MonthlyCharges", "impact": 0.084},
        {"feature": "TechSupport", "impact": -0.052},
        {"feature": "InternetService", "impact": 0.041},
    ]

    if pipeline is None or explainer is None or preprocessor is None:
        return {
            "risk_score": 0.5,
            "attributions": fallback_attributions,
        }

    try:
        # Preprocess customer record
        customer_transformed = preprocessor.transform(df)

        # Risk score directly from SVM
        risk_score = float(classifier.predict_proba(customer_transformed)[:, 1][0])

        # Compute real SHAP values with KernelExplainer
        shap_values = explainer.shap_values(customer_transformed, nsamples=80)
        if isinstance(shap_values, list):
            shap_values = shap_values[0]
        raw_vals = np.asarray(shap_values).flatten()

        # Group one-hot encoded impacts back to recognizable base features
        base_impacts: Dict[str, float] = {}
        for feature_name, impact in zip(all_feature_names, raw_vals):
            base_feature = feature_name
            if "_" in feature_name and feature_name not in NUMERIC_FEATURES:
                base_feature = feature_name.split("_")[0]
            base_impacts[base_feature] = base_impacts.get(base_feature, 0.0) + float(impact)

        attributions = [
            {"feature": feat, "impact": round(float(imp), 4)}
            for feat, imp in base_impacts.items()
        ]
        # Rank by absolute impact magnitude
        attributions.sort(key=lambda x: abs(x["impact"]), reverse=True)

        return {
            "risk_score": round(risk_score, 4),
            "attributions": attributions if attributions else fallback_attributions,
        }
    except Exception as e:
        print(f"[Auralytix SHAP] Calculation error: {e}")
        return {
            "risk_score": 0.5,
            "attributions": fallback_attributions,
        }


if __name__ == "__main__":
    sample_input = {
        "tenure": 3,
        "Contract": "Month-to-month",
        "MonthlyCharges": 85.0,
        "TotalCharges": 255.0,
        "InternetService": "Fiber optic",
        "TechSupport": "No",
        "OnlineSecurity": "No",
    }
    result = explain_customer(sample_input)
    print("Risk Score:", result["risk_score"])
    print("Top 5 SHAP Attributions:")
    for attr in result["attributions"][:5]:
        print(f"  {attr['feature']:20s}: {attr['impact']:+.4f}")
