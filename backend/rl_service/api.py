import sys
import datetime
import uuid
from pathlib import Path
from typing import List, Dict, Any, Optional

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from backend.db.database import get_db, SessionLocal
from backend.db.models import OutcomeModel, FeedbackModel, utc_now_iso
from backend.rl_service.agent import ContextualBanditAgent, ACTIONS, ACTION_LABELS

try:
    from backend.cloud.cloudwatch_service import record_intervention_metric
except Exception:
    record_intervention_metric = None

router = APIRouter()

POLICY_MODEL_VERSION = "policy-bandit-v2.0"

# Initialize Bandit Agent
bandit_agent = ContextualBanditAgent(actions=ACTIONS, alpha=0.7)

# Pre-train bandit agent on startup if outcomes exist in DB
try:
    _db = SessionLocal()
    _outcomes = _db.query(OutcomeModel).all()
    if _outcomes:
        _report = bandit_agent.train_from_outcomes(_outcomes)
        print(f"[Auralytix RL] Contextual Bandit initialized from {_report['trained_samples']} outcomes (Win rate: {_report['win_rate']*100:.1f}%)")
    _db.close()
except Exception as _e:
    print(f"[Auralytix RL] Notice initializing bandit from DB: {_e}")


class DecideRequest(BaseModel):
    customer_id: str
    customer_name: str
    risk_score: float
    risk_band: str
    top_attribution: str
    knowledge_response: str
    knowledge_confidence: float


class ActionScore(BaseModel):
    action: str
    score: float
    rationale: str


class PolicyDecision(BaseModel):
    customer_id: str
    customer_name: str
    risk_score: float
    risk_band: str
    top_attribution: str
    selected_action: str
    action_scores: List[ActionScore]
    knowledge_response: str
    knowledge_confidence: float
    model_version: str
    timestamp: str


@router.post("/decide", response_model=PolicyDecision)
def decide_action(req: DecideRequest):
    """
    Computes optimal retention action using the LinUCB Contextual Bandit policy.
    Scores all candidate actions dynamically based on customer risk state.
    """
    context_vec = bandit_agent.extract_features(
        risk_score=req.risk_score,
        risk_band=req.risk_band,
        top_attribution=req.top_attribution,
        confidence=req.knowledge_confidence,
    )

    selected_action, scored_actions = bandit_agent.predict_action_scores(context_vec)

    # CloudWatch Metric emission
    if record_intervention_metric is not None:
        try:
            record_intervention_metric(selected_action, success=True)
        except Exception as e:
            print(f"[RL API] CloudWatch metric error: {e}")

    return PolicyDecision(
        customer_id=req.customer_id,
        customer_name=req.customer_name,
        risk_score=req.risk_score,
        risk_band=req.risk_band,
        top_attribution=req.top_attribution,
        selected_action=selected_action,
        action_scores=[ActionScore(**s) for s in scored_actions],
        knowledge_response=req.knowledge_response,
        knowledge_confidence=req.knowledge_confidence,
        model_version=POLICY_MODEL_VERSION,
        timestamp=utc_now_iso(),
    )


class LogOutcomeRequest(BaseModel):
    decision: dict


@router.post("/outcome")
def log_outcome(req: LogOutcomeRequest, db: Session = Depends(get_db)):
    """Logs an initial intervention decision to the database with 'pending' status."""
    dec = req.decision
    outcome_id = f"out_{uuid.uuid4().hex[:8]}"
    now_iso = utc_now_iso()

    record = {
        "id": outcome_id,
        "customer_id": dec.get("customer_id", "unknown"),
        "customer_name": dec.get("customer_name", "Unknown"),
        "risk_score": float(dec.get("risk_score", 0.5)),
        "risk_band": dec.get("risk_band", "moderate"),
        "top_attribution": dec.get("top_attribution", "Contract"),
        "selected_action": dec.get("selected_action", "proactive_nudge"),
        "knowledge_response": dec.get("knowledge_response", ""),
        "confidence": float(dec.get("knowledge_confidence", 0.85)),
        "outcome": "pending",
        "created_at": now_iso,
        "resolved_at": None,
    }

    try:
        db_outcome = OutcomeModel(**record)
        db.add(db_outcome)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"[Auralytix RL] Error saving outcome to DB: {e}")

    return record


class UpdateOutcomeRequest(BaseModel):
    id: str
    outcome: str


@router.post("/outcome/update")
def update_outcome(req: UpdateOutcomeRequest, db: Session = Depends(get_db)):
    """
    Updates the outcome of an intervention (success / failure) and immediately
    feeds the reward signal back into the Contextual Bandit policy.
    """
    now_iso = utc_now_iso()
    db_record = db.query(OutcomeModel).filter(OutcomeModel.id == req.id).first()
    if not db_record:
        raise HTTPException(status_code=404, detail="Outcome record not found")

    db_record.outcome = req.outcome
    db_record.resolved_at = now_iso
    db.commit()

    # Online Policy Update (Closed Feedback Loop)
    reward = 1.0 if req.outcome == "success" else -0.8
    context_vec = bandit_agent.extract_features(
        risk_score=db_record.risk_score,
        risk_band=db_record.risk_band,
        top_attribution=db_record.top_attribution,
        confidence=db_record.confidence,
    )
    bandit_agent.update(db_record.selected_action, context_vec, reward)

    if record_intervention_metric is not None:
        try:
            record_intervention_metric(db_record.selected_action, success=(req.outcome == "success"))
        except Exception:
            pass

    return {
        "id": db_record.id,
        "customer_id": db_record.customer_id,
        "customer_name": db_record.customer_name,
        "risk_score": db_record.risk_score,
        "risk_band": db_record.risk_band,
        "top_attribution": db_record.top_attribution,
        "selected_action": db_record.selected_action,
        "outcome": db_record.outcome,
        "reward_applied": reward,
        "resolved_at": db_record.resolved_at,
    }


class FeedbackPayload(BaseModel):
    user_id: str
    action: str
    feedback: str


@router.post("/feedback")
def receive_feedback(payload: FeedbackPayload, db: Session = Depends(get_db)):
    """
    Records customer or CSM feedback, saves to database, and triggers real-time RL policy update.
    """
    # 1. Save to FeedbackModel
    fb_text = str(payload.feedback).lower()
    fb_entry = FeedbackModel(
        id=f"fb_{uuid.uuid4().hex[:8]}",
        customer_id=payload.user_id,
        action=payload.action,
        feedback=payload.feedback,
        created_at=utc_now_iso(),
    )
    try:
        db.add(fb_entry)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"[RL API] Error saving feedback: {e}")

    # 2. Determine reward signal from feedback sentiment
    positive_words = ["good", "great", "helpful", "retained", "success", "resolved", "solved", "positive", "1"]
    is_positive = any(w in fb_text for w in positive_words)
    reward = 1.0 if is_positive else -0.8

    # 3. Apply reward update to bandit agent
    context_vec = bandit_agent.extract_features(
        risk_score=0.65,
        risk_band="high",
        top_attribution="Contract",
        confidence=0.85,
    )
    bandit_agent.update(payload.action, context_vec, reward)

    if record_intervention_metric is not None:
        try:
            record_intervention_metric(payload.action, success=is_positive)
        except Exception:
            pass

    return {
        "status": "success",
        "message": f"Feedback recorded and RL policy updated (reward: {reward:+.1f})",
        "action": payload.action,
        "reward": reward,
        "total_policy_updates": bandit_agent.total_updates,
    }


@router.post("/retrain")
def retrain_policy(db: Session = Depends(get_db)):
    """
    Full retraining cycle: pulls all historical database outcomes and refits the Contextual Bandit.
    """
    outcomes = db.query(OutcomeModel).all()
    report = bandit_agent.train_from_outcomes(outcomes)

    return {
        "retrained": True,
        "model_version": POLICY_MODEL_VERSION,
        "samples_trained": report["trained_samples"],
        "win_rate": report["win_rate"],
        "total_updates": report["total_updates"],
        "timestamp": utc_now_iso(),
    }


@router.get("/aggregate")
def aggregate_outcomes(db: Session = Depends(get_db)):
    """
    Aggregates historical outcomes by retention action and root cause driver.
    """
    records = db.query(OutcomeModel).all()
    by_action = {}
    by_root = {}

    for r in records:
        act = r.selected_action
        if act not in by_action:
            by_action[act] = {"count": 0, "success_rate": 0.0}
        by_action[act]["count"] += 1

        root = r.top_attribution
        if root not in by_root:
            by_root[root] = {"count": 0, "riskSum": 0.0}
        by_root[root]["count"] += 1
        by_root[root]["riskSum"] += float(r.risk_score)

    for a in by_action.keys():
        acts = [r for r in records if r.selected_action == a]
        resolved = [r for r in acts if r.outcome != "pending"]
        success = len([r for r in resolved if r.outcome == "success"])
        by_action[a]["success_rate"] = round(success / len(resolved), 3) if resolved else 0.0

    def feature_label(feature: str) -> str:
        map_labels = {
            "Contract": "Contract term & pricing",
            "tenure": "Account tenure & maturity",
            "TechSupport": "Technical support availability",
            "InternetService": "Internet service stability",
            "MonthlyCharges": "Monthly charge sensitivity",
            "onboarding_confusion": "Onboarding confusion",
            "repeated_failures": "Repeated integration failures",
            "pricing_concern": "Pricing concern",
            "sentiment_decline": "Sentiment decline",
            "engagement_drop": "Engagement drop",
            "billing_anomaly": "Billing anomaly",
        }
        return map_labels.get(feature, feature)

    by_root_cause = []
    for feature, v in by_root.items():
        by_root_cause.append({
            "feature": feature,
            "label": feature_label(feature),
            "count": v["count"],
            "avg_risk": round(v["riskSum"] / v["count"], 3) if v["count"] else 0.0,
        })
    by_root_cause.sort(key=lambda x: x["count"], reverse=True)

    return {
        "total": len(records),
        "by_action": by_action,
        "by_root_cause": by_root_cause,
        "model_version": POLICY_MODEL_VERSION,
        "retrained": True,
        "last_retrain": utc_now_iso(),
    }
