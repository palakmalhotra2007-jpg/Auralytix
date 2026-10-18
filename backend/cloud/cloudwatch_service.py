import os
import time
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List
from dotenv import load_dotenv

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION", "ap-southeast-2")
CLOUDWATCH_NAMESPACE = os.getenv("CLOUDWATCH_NAMESPACE", "Auralytix/Production")
CLOUDWATCH_LOG_GROUP = os.getenv("CLOUDWATCH_LOG_GROUP", "/aws/auralytix/backend-logs")
CLOUDWATCH_LOG_STREAM = os.getenv("CLOUDWATCH_LOG_STREAM", f"api-server-{datetime.now().strftime('%Y%m%d')}")

_cw_client = None
_logs_client = None
_log_group_created = False
_log_stream_created = False

# In-memory buffer for local observability / simulation
_simulated_metrics: List[Dict[str, Any]] = []
_simulated_logs: List[Dict[str, Any]] = []


def get_cloudwatch_client():
    """Initializes and returns boto3 CloudWatch metrics client."""
    global _cw_client
    if _cw_client is not None:
        return _cw_client

    if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY:
        try:
            import boto3
            _cw_client = boto3.client(
                "cloudwatch",
                aws_access_key_id=AWS_ACCESS_KEY_ID,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                region_name=AWS_REGION,
            )
            return _cw_client
        except Exception as e:
            print(f"[AWS CloudWatch] Error initializing metrics client: {e}")
            return None
    return None


def get_logs_client():
    """Initializes and returns boto3 CloudWatch Logs client."""
    global _logs_client
    if _logs_client is not None:
        return _logs_client

    if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY:
        try:
            import boto3
            _logs_client = boto3.client(
                "logs",
                aws_access_key_id=AWS_ACCESS_KEY_ID,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                region_name=AWS_REGION,
            )
            return _logs_client
        except Exception as e:
            print(f"[AWS CloudWatch Logs] Error initializing logs client: {e}")
            return None
    return None


def is_cloudwatch_configured() -> bool:
    return bool(AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY)


def ensure_log_group_and_stream(client):
    """Ensures that the CloudWatch log group and daily stream exist."""
    global _log_group_created, _log_stream_created

    if not _log_group_created:
        try:
            client.create_log_group(logGroupName=CLOUDWATCH_LOG_GROUP)
            _log_group_created = True
        except client.exceptions.ResourceAlreadyExistsException:
            _log_group_created = True
        except Exception as e:
            # Check string representation if exact exception class mismatch
            if "ResourceAlreadyExistsException" in str(e):
                _log_group_created = True
            else:
                print(f"[AWS CloudWatch Logs] Notice creating log group: {e}")

    if not _log_stream_created:
        try:
            client.create_log_stream(
                logGroupName=CLOUDWATCH_LOG_GROUP,
                logStreamName=CLOUDWATCH_LOG_STREAM,
            )
            _log_stream_created = True
        except Exception as e:
            if "ResourceAlreadyExistsException" in str(e):
                _log_stream_created = True
            else:
                print(f"[AWS CloudWatch Logs] Notice creating log stream: {e}")


def put_metric(
    metric_name: str,
    value: float,
    unit: str = "None",
    dimensions: Optional[Dict[str, str]] = None,
) -> bool:
    """Publishes a custom metric to Amazon CloudWatch."""
    dim_list = []
    if dimensions:
        dim_list = [{"Name": k, "Value": str(v)} for k, v in dimensions.items()]

    client = get_cloudwatch_client()
    if client:
        try:
            client.put_metric_data(
                Namespace=CLOUDWATCH_NAMESPACE,
                MetricData=[
                    {
                        "MetricName": metric_name,
                        "Value": float(value),
                        "Unit": unit,
                        "Timestamp": datetime.now(timezone.utc),
                        "Dimensions": dim_list,
                    }
                ],
            )
            return True
        except Exception as e:
            print(f"[AWS CloudWatch] Error publishing metric '{metric_name}': {e}")

    # Fallback to in-memory observability
    _simulated_metrics.append({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "metric_name": metric_name,
        "value": value,
        "unit": unit,
        "dimensions": dimensions or {},
    })
    if len(_simulated_metrics) > 200:
        _simulated_metrics.pop(0)
    return True


def log_event(message: str, level: str = "INFO", extra: Optional[Dict[str, Any]] = None) -> bool:
    """Streams a log record to Amazon CloudWatch Logs."""
    timestamp_ms = int(time.time() * 1000)
    formatted_msg = f"[{level.upper()}] {message}"
    if extra:
        formatted_msg += f" | {extra}"

    client = get_logs_client()
    if client:
        try:
            ensure_log_group_and_stream(client)
            client.put_log_events(
                logGroupName=CLOUDWATCH_LOG_GROUP,
                logStreamName=CLOUDWATCH_LOG_STREAM,
                logEvents=[
                    {
                        "timestamp": timestamp_ms,
                        "message": formatted_msg,
                    }
                ],
            )
            return True
        except Exception as e:
            print(f"[AWS CloudWatch Logs] Error streaming log: {e}")

    # Fallback simulation
    _simulated_logs.append({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "level": level,
        "message": formatted_msg,
    })
    if len(_simulated_logs) > 200:
        _simulated_logs.pop(0)
    return True


def record_inference_metrics(latency_ms: float, risk_score: float, is_critical: bool) -> None:
    """Convenience helper: logs prediction event and records real-time latency and alert metrics."""
    # 1. Total predictions counter
    put_metric("ChurnPredictionCount", 1.0, unit="Count")

    # 2. Latency in milliseconds
    put_metric("ModelInferenceLatency", float(latency_ms), unit="Milliseconds")

    # 3. Critical alert counter if customer risk is high
    if is_critical or risk_score >= 0.75:
        put_metric("CriticalRiskAlerts", 1.0, unit="Count")

    # 4. Stream structured log event
    log_event(
        f"Inference completed in {latency_ms:.1f}ms - Risk: {risk_score:.4f} (Critical: {is_critical})",
        level="WARNING" if is_critical else "INFO",
        extra={"risk_score": risk_score, "latency_ms": round(latency_ms, 2)},
    )


def record_intervention_metric(action_name: str, success: bool = True) -> None:
    """Records retention intervention execution to CloudWatch."""
    put_metric(
        "InterventionExecutionCount",
        1.0,
        unit="Count",
        dimensions={"Action": action_name, "Success": str(success)},
    )
    log_event(
        f"Intervention triggered: '{action_name}' (Success: {success})",
        level="INFO",
        extra={"action": action_name, "success": success},
    )


def get_cloudwatch_status() -> Dict[str, Any]:
    """Returns connectivity and configuration status for AWS CloudWatch Metrics & Logs."""
    configured = is_cloudwatch_configured()
    cw_client = get_cloudwatch_client() if configured else None
    logs_client = get_logs_client() if configured else None

    cw_connected = False
    if cw_client:
        try:
            cw_client.list_metrics(Namespace=CLOUDWATCH_NAMESPACE)
            cw_connected = True
        except Exception:
            cw_connected = False

    return {
        "service": "Amazon CloudWatch",
        "configured": configured,
        "connected": cw_connected,
        "namespace": CLOUDWATCH_NAMESPACE,
        "log_group": CLOUDWATCH_LOG_GROUP,
        "log_stream": CLOUDWATCH_LOG_STREAM,
        "region": AWS_REGION,
        "mode": "AWS Live Cloud" if (configured and cw_connected) else "Local Simulation",
        "recent_metrics_buffered": len(_simulated_metrics),
        "recent_logs_buffered": len(_simulated_logs),
    }


def get_recent_telemetry() -> Dict[str, Any]:
    """Returns recent metrics and logs for the admin dashboard."""
    return {
        "status": get_cloudwatch_status(),
        "recent_metrics": _simulated_metrics[-20:],
        "recent_logs": _simulated_logs[-20:],
    }
