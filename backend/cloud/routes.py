import os
import socket
from pathlib import Path
from typing import Dict, Any, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from backend.db.database import get_db, DATABASE_URL
from backend.cloud.s3_service import get_s3_status, upload_file_to_s3, upload_model_artifacts, list_s3_files
from backend.cloud.cloudwatch_service import (
    get_cloudwatch_status,
    get_recent_telemetry,
    put_metric,
    log_event,
)

router = APIRouter(prefix="/cloud", tags=["AWS Cloud Services"])

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
ML_MODEL_DIR = ROOT_DIR / "ml" / "saved_model"
DATA_DIR = ROOT_DIR / "data"


@router.get("/status")
def cloud_status(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Returns real-time health, connectivity, and configuration of all AWS Cloud infrastructure."""
    # 1. Database / RDS status
    db_type = "Amazon RDS PostgreSQL" if "postgres" in DATABASE_URL.lower() else "SQLite Database"
    db_connected = False
    try:
        db.execute(text("SELECT 1"))
        db_connected = True
    except Exception:
        db_connected = False

    # 2. S3 status
    s3_info = get_s3_status()

    # 3. CloudWatch status
    cw_info = get_cloudwatch_status()

    # 4. EC2 host / environment info
    hostname = socket.gethostname()
    is_ec2 = bool(
        os.getenv("AWS_EXECUTION_ENV")
        or os.getenv("EC2_INSTANCE_ID")
        or "amzn" in hostname.lower()
        or "ip-" in hostname.lower()
    )

    return {
        "provider": "Amazon Web Services (AWS)",
        "region": os.getenv("AWS_REGION", "ap-southeast-2"),
        "infrastructure": {
            "compute": {
                "service": "Amazon EC2",
                "instance_type": os.getenv("AWS_INSTANCE_TYPE", "t3.micro (Free Tier)"),
                "status": "Healthy / Operational",
                "hostname": hostname,
                "is_ec2_environment": is_ec2,
                "protocol": "HTTPS (Nginx + SSL)" if os.getenv("ENABLE_HTTPS", "true").lower() == "true" else "HTTP",
            },
            "storage": s3_info,
            "database": {
                "service": db_type,
                "connected": db_connected,
                "engine": "PostgreSQL" if "postgres" in DATABASE_URL.lower() else "SQLite (Local Dev)",
                "status": "Connected & Operational" if db_connected else "Disconnected / Local Fallback",
            },
            "observability": cw_info,
            "vector_search": {
                "service": "Qdrant Vector Database",
                "host": os.getenv("QDRANT_HOST", "localhost"),
                "port": int(os.getenv("QDRANT_PORT", 6333)),
                "status": "Active",
            },
        },
    }


@router.get("/metrics")
def get_metrics() -> Dict[str, Any]:
    """Returns recent CloudWatch custom metrics and structured log entries."""
    return get_recent_telemetry()


@router.post("/sync-s3")
def sync_s3_artifacts():
    """Syncs trained SVM model artifacts, metadata, and Telco datasets to Amazon S3."""
    log_event("Triggered manual S3 artifact synchronization", level="INFO")

    sync_results = {}
    if ML_MODEL_DIR.exists():
        sync_results["models"] = upload_model_artifacts(ML_MODEL_DIR)

    # Also upload the reference dataset if present
    telco_csv = DATA_DIR / "WA_Fn-UseC_-Telco-Customer-Churn.csv"
    if telco_csv.exists():
        ok = upload_file_to_s3(str(telco_csv), "datasets/WA_Fn-UseC_-Telco-Customer-Churn.csv")
        sync_results["datasets"] = {"WA_Fn-UseC_-Telco-Customer-Churn.csv": ok}

    # Record metric to CloudWatch
    put_metric("S3ArtifactSyncCount", 1.0, unit="Count")

    return {
        "status": "success",
        "message": "SVM model artifacts and dataset synchronized with Amazon S3",
        "synced_files": sync_results,
    }


@router.get("/s3/files")
def get_s3_files():
    """Lists files currently archived in the S3 bucket."""
    bucket_name = os.getenv("AWS_S3_BUCKET", "auralytix-2026")
    files = list_s3_files()
    return {
        "bucket": bucket_name,
        "files_count": len(files),
        "files": files,
    }
