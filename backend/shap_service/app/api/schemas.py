from pydantic import BaseModel
from typing import List, Optional


class RiskRequest(BaseModel):
    # Existing PulseIQ signal fields (with defaults for Telco payloads)
    usage_decline: float = 0.4
    tickets_last30: int = 1
    negative_sentiment: float = 0.35
    feature_dropout: float = 0.3
    active_days: int = 4
    support_delay: float = 5.0
    payment_delay: float = 0.0

    # Optional Telco Customer Churn fields
    gender: Optional[str] = None
    SeniorCitizen: Optional[int] = None
    Partner: Optional[str] = None
    Dependents: Optional[str] = None
    tenure: Optional[int] = None
    PhoneService: Optional[str] = None
    MultipleLines: Optional[str] = None
    InternetService: Optional[str] = None
    OnlineSecurity: Optional[str] = None
    OnlineBackup: Optional[str] = None
    DeviceProtection: Optional[str] = None
    TechSupport: Optional[str] = None
    StreamingTV: Optional[str] = None
    StreamingMovies: Optional[str] = None
    Contract: Optional[str] = None
    PaperlessBilling: Optional[str] = None
    PaymentMethod: Optional[str] = None
    MonthlyCharges: Optional[float] = None
    TotalCharges: Optional[float] = None


class Attribution(BaseModel):
    feature: str
    impact: float


class RiskResponse(BaseModel):
    risk_score: float
    churn_probability: Optional[float] = None
    risk_category: Optional[str] = None
    attributions: List[Attribution]
    model_version: str
    timestamp: Optional[str] = None
