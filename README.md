# PulseIQ: Cloud-Native Autonomous AI Platform

PulseIQ is an intelligent, full-stack cloud platform for customer retention and proactive intervention. It integrates predictive neural network modeling, SHAP explainable AI, retrieval-augmented knowledge assistance, contextual reinforcement learning, and an interactive modern web dashboard.

---

## ⚡ Quick Start: Run the Application

You can run the entire application directly from this main folder with a single command:

```bash
npm install
npm run dev
```

Open **`http://localhost:5173`** in your browser.

- All AI subsystems (Risk & Behavior Engine, Knowledge Assistant, Action Policy, System Health) are instantly live.
- Zero complex Python virtual environment setup or Docker needed for local development.

---

## 📂 Repository Structure

The project has a clean, unified structure in the root directory:

```
PulseIQ/
├── src/                      # Application source code
│   ├── components/           # UI components, views, 3D visualizers, layouts
│   ├── hooks/                # React custom hooks
│   ├── lib/                  # AI orchestrator, risk engine, RAG client, action policy
│   ├── server/               # Embedded dev API server & simulated endpoints
│   ├── App.tsx               # Main application entry component
│   ├── index.css             # Tailwind styling & dark-mode design system
│   └── main.tsx              # React DOM mounting
├── public/                   # Static assets, 3D neural network canvas, icons
├── index.html                # Main single-page web entry point
├── package.json              # Scripts (`npm run dev`, `build`) and dependencies
├── vite.config.ts            # Vite bundler with integrated API middleware
├── tailwind.config.js        # Modern design system tokens & colors
├── tsconfig.json             # TypeScript configuration
├── cloud/                    # AWS Infrastructure-as-Code (CloudFormation)
├── docs/                     # Pitch decks and project documentation
└── docker-compose.yml        # Multi-container orchestration
```

---

## 🏗️ Architecture & Core Subsystems

1. **Risk & Behavior Engine (`src/lib/riskEngine.ts`)**
   - Evaluates customer behavior signals (login frequency, ticket escalations, sentiment drops) and outputs signed SHAP feature attribution vectors.

2. **Grounded Knowledge Assistant (`src/lib/knowledgeAssistant.ts`)**
   - Retrieves relevant playbooks and documents with citation validation and hallucination-free grounded guidance.

3. **Contextual Action Policy (`src/lib/actionPolicy.ts`)**
   - Softmax reinforcement learning policy mapping the dominant root-cause attribution to high-EV interventions (guided tutorials, proactive nudges, human handoffs, or loyalty incentives).

4. **Integrated Dev API Server (`src/server/devApiServer.ts`)**
   - Built directly into Vite's dev server to instantly fulfill all `/health`, `/shap/*`, `/rag/*`, `/policy/*`, and `/api/*` endpoints with zero latency.

---

## 📡 API Endpoints Reference

| Endpoint | Method | Subsystem | Description |
|---|---|---|---|
| `/health` | GET | System | Health check and live system status |
| `/api/customers` | GET | Customers | Retrieve customer profiles and signal metrics |
| `/shap/risk/score` | POST | SHAP Engine | Compute churn risk and feature attributions |
| `/rag/knowledge/respond` | POST | RAG Assistant | Contextual document retrieval & grounded guidance |
| `/policy/decide` | POST | RL Policy | Softmax action policy recommendation |
| `/policy/outcome` | POST | RL Policy | Log intervention outcome to feedback loop |
| `/policy/aggregate` | GET | RL Policy | Root-cause aggregation and success rates |
| `/policy/retrain` | POST | RL Policy | Trigger policy retraining simulation |

---

## 🧪 Build & Verification

```bash
# Verify TypeScript types and build production bundle
npm run build
```

---

## License

MIT License. Open source for cloud deployment and portfolio evaluation.
