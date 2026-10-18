import joblib
import torch
import pandas as pd
from pathlib import Path
import sys

# Add root directory to path
ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

MODEL_DIR = Path(__file__).resolve().parent

try:
    from ml.inference import predict_churn
except Exception:
    predict_churn = None

# Legacy PyTorch risk model loading
scaler = None
model = None

try:
    from app.models.model import RiskPredictionModel
    if (MODEL_DIR / "scaler.pkl").exists() and (MODEL_DIR / "risk_model.pth").exists():
        scaler = joblib.load(MODEL_DIR / "scaler.pkl")
        INPUT_SIZE = 7
        model = RiskPredictionModel(INPUT_SIZE)
        model.load_state_dict(
            torch.load(
                MODEL_DIR / "risk_model.pth",
                map_location=torch.device("cpu")
            )
        )
        model.eval()
except Exception as e:
    print(f"[Auralytix Model] Legacy torch model note: {e}")


def predict_risk(customer_features):
    """
    Predict churn risk score. Prioritizes the scikit-learn Support Vector Machine (SVM RBF)
    pipeline in ml/saved_model, and falls back to legacy torch model.
    """
    columns = [
        "usage_decline",
        "tickets_last30",
        "negative_sentiment",
        "feature_dropout",
        "active_days",
        "support_delay",
        "payment_delay"
    ]

    if isinstance(customer_features, (list, tuple)):
        features_dict = dict(zip(columns, customer_features))
    elif isinstance(customer_features, dict):
        features_dict = customer_features
    else:
        features_dict = {}

    if predict_churn is not None:
        try:
            res = predict_churn(features_dict)
            return float(res["churn_probability"])
        except Exception as e:
            print(f"[Auralytix Model] Inference error via ml.inference: {e}")

    if model is not None and scaler is not None:
        try:
            df = pd.DataFrame([customer_features], columns=columns)
            scaled = scaler.transform(df)
            tensor = torch.FloatTensor(scaled)
            with torch.no_grad():
                risk_score = model(tensor)
            return float(risk_score.item())
        except Exception as e:
            print(f"[Auralytix Model] Legacy torch inference error: {e}")

    # Fallback heuristic
    return float(min(0.95, max(0.05, features_dict.get("usage_decline", 0.5) * 0.8 + 0.1)))


if __name__ == "__main__":
    sample_customer = [
        0.55,
        3,
        0.72,
        0.60,
        2,
        14,
        3
    ]
    print(f"Predicted Risk Score: {predict_risk(sample_customer):.4f}")
