# Auralytix: Cloud-Native Autonomous AI Platform

Auralytix is an intelligent, full-stack cloud platform for proactive customer retention and intervention. It integrates predictive Machine Learning churn modeling, SHAP explainable AI, retrieval-augmented knowledge assistance, contextual reinforcement learning, and a modern reactive dashboard.

---

## 🏛️ Cloud Architecture (AWS Free Tier Eligible)

The system is architected for seamless deployment across AWS Free Tier services:

```text
+----------------------------------------------------------------------------------------------------+
|                                    AWS Cloud (Free Tier)                                           |
|                                                                                                    |
|  +-----------------------------+                  +---------------------------------------------+  |
|  |      Amazon S3 Storage      |                  |             Amazon RDS PostgreSQL           |  |
|  | - Model Artifacts Bucket    |                  |           (db.t3.micro / db.t4g.micro)      |  |
|  | - Knowledge Base Docs Bucket|                  | - customers table                           |  |
|  | - Generated Reports & Plots |                  | - risk_scores table                         |  |
|  +-----------------------------+                  | - outcomes table                            |  |
|                 ^                                 | - feedback table                            |  |
|                 | boto3                           +---------------------------------------------+  |
|                 v                                                        ^                         |
|  +-----------------------------------------------------------------------|----------------------+  |
|  |                        Amazon EC2 Instance (t2.micro / t3.micro)      |                      |  |
|  |                                                                       |                      |  |
|  |  +-------------------------+             +-------------------------+  |                      |  |
|  |  |     FastAPI Backend     |<----------->|     Qdrant Vector DB    |  |                      |  |
|  |  |   (SHAP + RAG + RL + DB)|             |  (Docker Container:6333)|  |                      |  |
|  |  +-------------------------+             +-------------------------+  |                      |  |
|  |                 ^                                                     |                      |  |
|  |                 | Nginx Reverse Proxy (Port 80/443)                   |                      |  |
|  |                 v                                                     |                      |  |
|  |  +-------------------------+                                          |                      |  |
|  |  |   React SPA Frontend    |                                          |                      |  |
|  |  |    (Production Dist)    |                                          |                      |  |
|  |  +-------------------------+                                          |                      |  |
|  +----------------------------------------------------------------------------------------------+  |
+----------------------------------------------------------------------------------------------------+
```

- **Amazon EC2 (`t2.micro` / `t3.micro`)**: Hosts the Docker container cluster:
  - **Nginx Reverse Proxy**: Listens on Port 80/443 and serves the React SPA production distribution, proxying API calls to backend.
  - **FastAPI Unified Backend**: Port 8000 handling SHAP explainability, ML churn prediction, RAG document retrieval, and RL action policies.
  - **Qdrant Vector Database**: Port 6333 for dense vector indexing and cosine similarity retrieval.
- **Amazon S3**: Stores fitted model pipelines (`churn_pipeline.joblib`), evaluation reports, and raw knowledge base documents via `boto3`.
- **Amazon RDS PostgreSQL (`db.t3.micro`)**: Cloud-managed persistence for customer records, risk scores, attributions, intervention outcomes, and feedback loop logs.

---

## ⚡ Local Development: Single-Command Quick Start

You can run the entire application directly from the root repository directory with zero setup:

```bash
# 1. Install dependencies
npm install

# 2. Start the integrated dev server
npm run dev
```

Open **`http://localhost:5173`** in your browser.
- All AI subsystems (Risk & Behavior Engine, Knowledge Assistant, Action Policy, Feedback Loop, System Health) are instantly operational via the integrated dev API server.
- Zero complex Python virtual environment or Docker containers required for local frontend development.

---

## 🚀 AWS EC2 Deployment Guide

### Option 1: Automated 1-Click Launch with CloudFormation

1. Navigate to the **AWS CloudFormation Console** in your AWS region (e.g. `us-east-1`).
2. Click **Create stack (with new resources)**.
3. Upload the template [`cloud/cloudformation.yml`](file:///cloud/cloudformation.yml).
4. Specify parameters:
   - `InstanceType`: `t3.micro` or `t2.micro` (AWS Free Tier).
   - `S3BucketName`: Unique bucket name (e.g., `auralytix-artifacts-<your-id>`).
   - `DBPassword`: Strong password for the Amazon RDS PostgreSQL instance.
5. Click **Submit**. CloudFormation automatically provisions:
   - Amazon S3 Bucket
   - Amazon RDS PostgreSQL (`db.t3.micro`)
   - EC2 Instance with IAM role and Security Groups
   - Clones this GitHub repo, writes configuration, and launches all containers.
6. Open the `FrontendURL` output in your browser!

---

### Option 2: Deploying to an Existing EC2 Instance

1. Launch an AWS EC2 instance (`t3.micro` or `t2.micro` running Amazon Linux 2023 or Ubuntu 24.04).
2. Attach a Security Group with ports `80`, `443`, `8000`, and `22` open.
3. In the EC2 **User Data** field, paste the contents of [`cloud/ec2-user-data.sh`](file:///cloud/ec2-user-data.sh).
4. Launch the instance. The script will automatically install Docker, clone the repository, and start all containers.

---

### Option 3: Manual Deployment on EC2 via Docker Compose

SSH into your EC2 instance and run:

```bash
# Clone the repository
git clone https://github.com/palakmalhotra2007-jpg/Auralytix.git /opt/auralytix
cd /opt/auralytix

# Configure environment variables (optional: connect to RDS or use container DB)
cp .env.example .env

# Build and start all containers
docker compose up -d --build
```

Access the application:
- **Web Dashboard**: `http://<EC2-PUBLIC-IP>`
- **FastAPI Swagger Docs**: `http://<EC2-PUBLIC-IP>:8000/docs`
- **Qdrant Vector DB**: `http://<EC2-PUBLIC-IP>:6333/dashboard`

---

## 🤖 ML Churn Pipeline (`ml/`)

The repository includes a production scikit-learn churn prediction pipeline trained on Telco customer churn data:

```bash
# Train the model and evaluate precision, recall, F1, and ROC-AUC
python ml/train.py --data-path data/WA_Fn-UseC_-Telco-Customer-Churn.csv
```

- Model Artifacts: `ml/saved_model/churn_pipeline.joblib`
- Metadata: `ml/saved_model/model_metadata.json`
- In-memory inference engine: `ml/inference.py`

---

## 📡 API Endpoints Reference

| Endpoint | Method | Subsystem | Description |
|---|---|---|---|
| `/health` | GET | System | Live health check and subsystem status |
| `/api/customers` | GET | Database | Retrieve customer records and signal metrics |
| `/shap/risk/score` | POST | ML + SHAP | Churn probability prediction & feature attributions |
| `/rag/knowledge/respond` | POST | RAG | Document retrieval & grounded AI guidance |
| `/policy/decide` | POST | RL Policy | Softmax action policy recommendation |
| `/policy/outcome` | POST | Feedback | Log intervention outcome for RL retraining |
| `/policy/aggregate` | GET | Feedback | Root-cause distribution and resolution stats |
| `/policy/retrain` | POST | Feedback | Trigger policy retraining simulation |
| `/cloud/status` | GET | Cloud | AWS S3 and RDS connection status |

---

## 🧪 Production Verification

```bash
# Build production bundle
npm run build
```

---

## License

MIT License. Open source for cloud deployment and portfolio evaluation.
