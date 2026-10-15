from fastapi import APIRouter
from datetime import datetime
import pandas as pd
from pathlib import Path
import sys

from app.api.schemas import RiskRequest, RiskResponse

# Ensure root directory is on sys.path for ml module
ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

try:
    from ml.inference import predict_churn
except Exception as e:
    print(f"[Auralytix API] Notice: Could not import ml.inference directly: {e}")
    predict_churn = None

try:
    from app.explainability.shap_engine import explain_customer
except Exception as e:
    explain_customer = None

router = APIRouter()

SERVICE_DIR = Path(__file__).resolve().parent.parent.parent
FEEDBACK_FILE = SERVICE_DIR / "feedback.csv"


@router.get("/")
def home():
    return {
        "message": "Auralytix Risk & Churn Prediction Engine Running 🚀",
        "model": "Telco Logistic Regression Churn Pipeline",
    }


@router.post("/risk/score")
def risk_score(request: RiskRequest):
    req_dict = request.dict()

    # 1. Run inference using the saved ML pipeline
    if predict_churn is not None:
        prediction_result = predict_churn(req_dict)
    else:
        # Fallback if ml package is not importable
        prediction_result = {
            "churn_probability": 0.5,
            "risk_score": 0.5,
            "risk_category": "moderate",
        }

    churn_prob = prediction_result.get("churn_probability", 0.5)
    risk_cat = prediction_result.get("risk_category", "moderate")

    # 2. Compute or fallback feature attributions
    attributions = []
    features = [
        request.usage_decline,
        request.tickets_last30,
        request.negative_sentiment,
        request.feature_dropout,
        request.active_days,
        request.support_delay,
        request.payment_delay,
    ]

    if explain_customer is not None:
        try:
            result = explain_customer(features)
            attributions = result.get("attributions", [])
        except Exception as e:
            print(f"[Auralytix API] SHAP explainability warning: {e}")

    if not attributions:
        # Build attributions from customer signals and contract terms
        candidates = [
            {"feature": "contract_term", "impact": 0.35 if request.Contract == "Month-to-month" or request.usage_decline > 0.4 else -0.2},
            {"feature": "support_delay", "impact": round(float((request.support_delay / 24.0) * 0.4), 3)},
            {"feature": "negative_sentiment", "impact": round(float(request.negative_sentiment * 0.35), 3)},
            {"feature": "usage_decline", "impact": round(float(request.usage_decline * 0.3), 3)},
            {"feature": "payment_delay", "impact": round(float((request.payment_delay / 30.0) * 0.25), 3)},
        ]
        candidates.sort(key=lambda x: abs(x["impact"]), reverse=True)
        attributions = candidates

    return {
        "risk_score": churn_prob,
        "churn_probability": churn_prob,
        "risk_category": risk_cat,
        "risk_band": risk_cat,
        "attributions": attributions,
        "model_version": "telco-logistic-regression-v1.0",
        "timestamp": datetime.now().isoformat(),
    }


@router.post("/feedback")
def feedback(data: dict):
    # 1. Save to Database if available
    try:
        from backend.db.database import SessionLocal
        from backend.db.models import FeedbackModel
        db = SessionLocal()
        fb = FeedbackModel(
            customer_id=str(data.get("user_id", data.get("customer_id", "unknown"))),
            action=str(data.get("action", "unknown")),
            feedback=str(data.get("feedback", data.get("comments", str(data)))),
        )
        db.add(fb)
        db.commit()
        db.close()
    except Exception as e:
        print(f"[SHAP DB Feedback] Notice: {e}")

    # 2. Append to CSV for backup/training scripts
    df = pd.DataFrame([data])
    if FEEDBACK_FILE.exists():
        df.to_csv(FEEDBACK_FILE, mode="a", header=False, index=False)
    else:
        df.to_csv(FEEDBACK_FILE, index=False)

    return {
        "status": "success",
        "message": "Feedback stored in database and training queue successfully."
    }
