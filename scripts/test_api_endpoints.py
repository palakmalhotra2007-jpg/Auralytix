import urllib.request
import json
import gzip

BASE_URL = "http://13.239.41.80"

def test_endpoint(name, method, path, data=None, accept_gzip=False):
    url = f"{BASE_URL}{path}"
    headers = {"Content-Type": "application/json"}
    if accept_gzip:
        headers["Accept-Encoding"] = "gzip"
    
    body = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            content = resp.read()
            encoding = resp.headers.get("Content-Encoding")
            if encoding == "gzip":
                content = gzip.decompress(content)
            print(f"[OK] {name} ({method} {path}) -> Status {resp.status}, Size {len(content)} bytes")
            try:
                snippet = json.loads(content.decode("utf-8"))
                if isinstance(snippet, list):
                    print(f"     Items count: {len(snippet)}")
                elif isinstance(snippet, dict):
                    print(f"     Keys: {list(snippet.keys())[:5]}")
            except Exception:
                print(f"     Snippet: {content.decode('utf-8', errors='ignore')[:80]}")
    except Exception as e:
        print(f"[FAIL] {name} ({method} {path}) -> Error: {e}")

if __name__ == "__main__":
    print(f"Testing all endpoints against {BASE_URL}...\n")
    test_endpoint("Health check", "GET", "/health")
    test_endpoint("Customers List", "GET", "/api/customers")
    test_endpoint("SHAP Risk Score", "POST", "/shap/risk/score", {
        "customer_id": "c_001",
        "tenure": 12,
        "MonthlyCharges": 75.0,
        "TotalCharges": 900.0,
        "Contract": "Month-to-month",
        "TechSupport": "No",
        "OnlineSecurity": "No"
    })
    test_endpoint("Policy Decide", "POST", "/policy/decide", {
        "customer_id": "c_001",
        "risk_score": 0.82,
        "primary_driver": "high_charges",
        "context": {}
    })
    test_endpoint("Policy Aggregate", "GET", "/policy/aggregate")
    test_endpoint("Policy Outcomes", "GET", "/policy/outcomes")
    test_endpoint("RAG Respond", "POST", "/rag/knowledge/respond", {
        "query": "How do we reduce customer churn?",
        "context": ""
    })
    test_endpoint("RL Feedback (Policy)", "POST", "/policy/feedback", {
        "action_id": "act_test",
        "customer_id": "c_001",
        "feedback": "Customer accepted discount offer and renewed."
    })
    test_endpoint("HTML Root", "GET", "/")
    test_endpoint("CSS Bundle (gzip)", "GET", "/assets/index-Yog9h5O5.css", accept_gzip=True)
    test_endpoint("JS Bundle (gzip)", "GET", "/assets/index-DENylRvh.js", accept_gzip=True)
