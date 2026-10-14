import os
import json
from pathlib import Path
from typing import Dict, Any, Union

import pandas as pd
import numpy as np

try:
    import joblib
except ImportError:
    joblib = None

MODEL_DIR = Path(__file__).resolve().parent / "saved_model"
MODEL_PATH = MODEL_DIR / "churn_pipeline.joblib"
METADATA_PATH = MODEL_DIR / "model_metadata.json"

_cached_pipeline = None


def get_risk_category(probability: float) -> str:
    """Categorizes churn probability into risk tiers."""
    if probability >= 0.75:
        return "critical"
    elif probability >= 0.55:
        return "high"
    elif probability >= 0.35:
        return "moderate"
    return "low"


def load_model():
    """Loads the fitted model pipeline from ml/saved_model."""
    global _cached_pipeline
    if _cached_pipeline is not None:
        return _cached_pipeline

    if not os.path.exists(MODEL_PATH) or joblib is None:
        return None

    try:
        _cached_pipeline = joblib.load(MODEL_PATH)
        return _cached_pipeline
    except Exception as e:
        print(f"[PulseIQ ML] Warning loading model from {MODEL_PATH}: {e}")
        return None


def map_legacy_features_to_telco(features: Dict[str, Any]) -> Dict[str, Any]:
    """
    Maps legacy PulseIQ feature dictionary to Telco customer churn dataset columns
    to preserve backward compatibility with existing API contracts.
    """
    usage_decline = float(features.get("usage_decline", 0.4))
    tickets_last30 = int(features.get("tickets_last30", 1))
    negative_sentiment = float(features.get("negative_sentiment", 0.35))
    feature_dropout = float(features.get("feature_dropout", 0.3))
    active_days = int(features.get("active_days", 4))
    support_delay = float(features.get("support_delay", 5.0))
    payment_delay = float(features.get("payment_delay", 0.0))

    tenure = max(1, min(72, int((active_days / 7.0) * 40 * (1.2 - usage_decline))))
    monthly_charges = round(float(40.0 + (tickets_last30 * 12.0) + (negative_sentiment * 30.0)), 2)
    total_charges = round(float(tenure * monthly_charges), 2)

    contract = (
        "Month-to-month"
        if usage_decline > 0.45 or payment_delay > 2
        else ("One year" if usage_decline > 0.25 else "Two year")
    )
    internet_service = "Fiber optic" if negative_sentiment > 0.4 else ("DSL" if negative_sentiment > 0.15 else "No")
    tech_support = "No" if support_delay > 12 else "Yes"
    online_security = "No" if feature_dropout > 0.5 else "Yes"
    payment_method = "Electronic check" if payment_delay > 1 else "Bank transfer (automatic)"

    return {
        "gender": features.get("gender", "Female"),
        "SeniorCitizen": int(features.get("SeniorCitizen", 0)),
        "Partner": features.get("Partner", "No"),
        "Dependents": features.get("Dependents", "No"),
        "tenure": tenure,
        "PhoneService": features.get("PhoneService", "Yes"),
        "MultipleLines": features.get("MultipleLines", "No"),
        "InternetService": internet_service,
        "OnlineSecurity": online_security,
        "OnlineBackup": features.get("OnlineBackup", "No"),
        "DeviceProtection": features.get("DeviceProtection", "No"),
        "TechSupport": tech_support,
        "StreamingTV": features.get("StreamingTV", "No"),
        "StreamingMovies": features.get("StreamingMovies", "No"),
        "Contract": contract,
        "PaperlessBilling": features.get("PaperlessBilling", "Yes"),
        "PaymentMethod": payment_method,
        "MonthlyCharges": monthly_charges,
        "TotalCharges": total_charges,
    }


def predict_churn(customer_data: Union[Dict[str, Any], pd.DataFrame]) -> Dict[str, Any]:
    """
    Predicts churn probability and assigns risk category using the saved pipeline.
    """
    pipeline = load_model()

    if isinstance(customer_data, dict):
        # Detect if input is using legacy features or Telco features
        if "usage_decline" in customer_data and "Contract" not in customer_data:
            input_dict = map_legacy_features_to_telco(customer_data)
        else:
            input_dict = customer_data
        df = pd.DataFrame([input_dict])
    else:
        df = customer_data.copy()

    # If TotalCharges is string, coerce to numeric
    if "TotalCharges" in df.columns:
        df["TotalCharges"] = pd.to_numeric(df["TotalCharges"].astype(str).str.strip(), errors="coerce").fillna(0.0)

    if pipeline is not None:
        try:
            probabilities = pipeline.predict_proba(df)[:, 1]
            prob = float(probabilities[0])
            category = get_risk_category(prob)
            return {
                "churn_probability": round(prob, 4),
                "risk_score": round(prob, 4),
                "risk_category": category,
                "risk_band": category,
                "model_status": "fitted_pipeline",
            }
        except Exception as e:
            print(f"[PulseIQ ML] Inference error through pipeline: {e}")

    # Fallback heuristic if model is not yet trained/available on disk
    tenure = float(df.get("tenure", [12])[0])
    contract = str(df.get("Contract", ["Month-to-month"])[0])
    monthly = float(df.get("MonthlyCharges", [70.0])[0])

    base_prob = 0.5
    if contract == "Month-to-month":
        base_prob += 0.25
    elif contract == "Two year":
        base_prob -= 0.3
    if tenure < 6:
        base_prob += 0.15
    if monthly > 80:
        base_prob += 0.1

    fallback_prob = max(0.05, min(0.95, base_prob))
    cat = get_risk_category(fallback_prob)
    return {
        "churn_probability": round(fallback_prob, 4),
        "risk_score": round(fallback_prob, 4),
        "risk_category": cat,
        "risk_band": cat,
        "model_status": "untrained_fallback",
    }
