import os
import sys
import json
import uuid
import random
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime, timezone, timedelta

# Ensure project root is in sys.path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import pandas as pd
from backend.db.database import SessionLocal, init_db, engine
from backend.db.models import CustomerModel, RiskScoreModel, OutcomeModel, FeedbackModel, utc_now_iso, Base
from ml.inference import predict_churn

DATA_PATH = BASE_DIR / "data" / "WA_Fn-UseC_-Telco-Customer-Churn.csv"

COMPANIES = [
    ("Northwind Robotics", "maya@northwind.io", "Maya Chen"),
    ("Lumen Health", "diego@lumenhealth.com", "Diego Alvarez"),
    ("Atlas Freight", "priya@atlasfreight.co", "Priya Nair"),
    ("Brightwave Media", "sam@brightwave.tv", "Sam Okafor"),
    ("Vertex Labs", "hana@vertexlabs.ai", "Hana Kobayashi"),
    ("Cedar & Co", "lucas@cedarco.com", "Lucas Pereira"),
    ("Skyline Energy", "aaliyah@skyline.energy", "Aaliyah Brooks"),
    ("Quantum Gear", "theo@quantumgear.de", "Theo Müller"),
    ("Harbor Pay", "ines@harborpay.io", "Ines Garcia"),
    ("Nimbus Cloud", "ravi@nimbus.cloud", "Ravi Shankar"),
    ("Polar Foods", "greta@polarfoods.se", "Greta Lindholm"),
    ("Sable Logistics", "omar@sablelog.com", "Omar Haddad"),
    ("Apex Dynamics", "elena@apexdynamics.com", "Elena Rostova"),
    ("BlueShift AI", "marcus@blueshift.ai", "Marcus Vance"),
    ("Strata Capital", "sophia@stratacap.com", "Sophia Sterling"),
    ("Vanguard Health", "kenji@vanguardhealth.jp", "Kenji Sato"),
    ("Zenith Networks", "clara@zenithnet.co", "Clara Dupont"),
    ("Cascade Analytics", "liam@cascadeanalytics.io", "Liam O'Connor"),
    ("Frontier Defense", "tariq@frontierdefense.ae", "Tariq Mansoor"),
    ("Meridian Biotech", "ananya@meridianbio.in", "Ananya Sharma"),
    ("Pulse Gaming", "charlie@pulsegame.tv", "Charlie Zhang"),
    ("Solstice Solar", "astrid@solsticesolar.no", "Astrid Lind"),
    ("AeroStream", "mateo@aerostream.aero", "Mateo Silva"),
    ("Prism Security", "zoe@prismsec.tech", "Zoe Bennett"),
    ("Ironclad Logistics", "viktor@ironcladlog.ru", "Viktor Kozlov"),
    ("Beacon Commerce", "nadia@beaconcommerce.com", "Nadia Fassi"),
    ("Catalyst Labs", "hugo@catalystlabs.fr", "Hugo Laurent"),
    ("Kinetix Fitness", "sienna@kinetixfit.com", "Sienna Miller"),
    ("Hyperion Compute", "arjun@hyperioncomp.com", "Arjun Patel"),
    ("Oasis Renewable", "fatima@oasisrenew.com", "Fatima Al-Hassan"),
    ("Nova Genomics", "gabriel@novagenomics.br", "Gabriel Costa"),
    ("Crestview Media", "olivia@crestview.co.uk", "Olivia Hughes"),
    ("Titanium Cloud", "dmitri@titaniumcloud.ee", "Dmitri Volkov"),
    ("Summit Hospitality", "amelia@summithotels.ch", "Amelia Rossi"),
    ("Aegis Cyber", "khalil@aegiscyber.qa", "Khalil Qasim"),
    ("Cobalt Robotics", "yuki@cobaltrobotics.jp", "Yuki Tanaka"),
    ("Echo Financial", "sebastian@echofin.de", "Sebastian Weber"),
    ("Vortex Energy", "leila@vortexenergy.ca", "Leila Haddad"),
    ("Horizon Space", "owen@horizonspace.io", "Owen Wright"),
    ("Optima Pharma", "valeria@optimapharma.es", "Valeria Morales"),
    ("Terra Agriculture", "kwame@terraagri.gh", "Kwame Mensah"),
    ("Labyrinth Security", "freja@labyrinthsec.dk", "Freja Nielsen"),
    ("Equinox Media", "dante@equinoxmedia.it", "Dante Moretti"),
    ("Starlight SaaS", "elizabeth@starlightapp.com", "Elizabeth Taylor"),
    ("Nautilus Marine", "connor@nautilusmarine.au", "Connor MacLeod"),
    ("Pinnacle AI", "mei@pinnacleai.sg", "Mei-Ling Zhou"),
    ("Solaris CleanTech", "lars@solarisclean.se", "Lars Berg"),
    ("Cipher Systems", "nadine@ciphersys.nl", "Nadine De Jong"),
    ("Aura Health", "carlos@aurahealth.mx", "Carlos Mendoza"),
    ("Apex Global", "rachel@apexglobal.com", "Rachel Adams"),
]


def generate_real_customer_records(count: int = 50) -> List[Dict[str, Any]]:
    """
    Extracts real demographic and contract data from the Telco dataset,
    runs the SVM model to compute genuine churn probabilities and risk bands,
    and maps them to enterprise customer profiles.
    """
    if not DATA_PATH.exists():
        print(f"[Seed] Warning: Dataset not found at {DATA_PATH}, using synthetic fallback.")
        df = pd.DataFrame()
    else:
        df = pd.read_csv(DATA_PATH)
        df["TotalCharges"] = pd.to_numeric(df["TotalCharges"].astype(str).str.strip(), errors="coerce").fillna(0.0)

    customers = []
    num_samples = min(count, len(COMPANIES))

    # Sample rows from Telco dataset (mix of churners and non-churners for balanced tiers)
    if not df.empty:
        churners = df[df["Churn"] == "Yes"].sample(n=min(20, len(df[df["Churn"] == "Yes"])), random_state=42)
        retained = df[df["Churn"] == "No"].sample(n=min(num_samples - len(churners), len(df[df["Churn"] == "No"])), random_state=42)
        telco_sample = pd.concat([churners, retained]).sample(frac=1.0, random_state=42).reset_index(drop=True)
    else:
        telco_sample = pd.DataFrame()

    for i in range(num_samples):
        cid = f"c_{i+1:03d}"
        company, email, name = COMPANIES[i]

        if not telco_sample.empty and i < len(telco_sample):
            row = telco_sample.iloc[i].to_dict()
            tenure_months = max(1, int(row.get("tenure", 12)))
            monthly_charges = float(row.get("MonthlyCharges", 70.0))
            total_charges = float(row.get("TotalCharges", tenure_months * monthly_charges))
            contract = str(row.get("Contract", "Month-to-month"))
            internet_service = str(row.get("InternetService", "Fiber optic"))
            tech_support = str(row.get("TechSupport", "No"))
            online_security = str(row.get("OnlineSecurity", "No"))
            payment_method = str(row.get("PaymentMethod", "Electronic check"))
        else:
            tenure_months = 12
            monthly_charges = 70.0
            total_charges = 840.0
            contract = "Month-to-month"
            internet_service = "Fiber optic"
            tech_support = "No"
            online_security = "No"
            payment_method = "Electronic check"

        # Tier assignment based on spend
        if monthly_charges >= 85:
            tier = "Enterprise"
            plan_value = 12000.0
        elif monthly_charges >= 55:
            tier = "Growth"
            plan_value = 4500.0
        else:
            tier = "Starter"
            plan_value = 990.0

        # Run SVM model prediction on this customer
        telco_input = {
            "tenure": tenure_months,
            "MonthlyCharges": monthly_charges,
            "TotalCharges": total_charges,
            "Contract": contract,
            "InternetService": internet_service,
            "TechSupport": tech_support,
            "OnlineSecurity": online_security,
            "PaymentMethod": payment_method,
        }
        pred = predict_churn(telco_input)
        risk_score = float(pred.get("risk_score", 0.5))
        risk_band = str(pred.get("risk_band", "moderate"))

        # Formulate behavioral signals calibrated with SVM risk score
        login_freq = max(0.08, min(0.98, 1.0 - (risk_score * 0.75)))
        tickets_count = int(round(risk_score * 7))
        sentiment = max(0.15, min(0.95, round(1.0 - (risk_score * 0.8), 2)))
        feature_adopt = max(0.12, min(0.96, round(1.0 - (risk_score * 0.7), 2)))
        billing_flag = 1 if (risk_score > 0.65 or payment_method == "Electronic check" and random.random() > 0.5) else 0
        onboarding_steps = min(6, max(1, int(tenure_months / 4)))

        signals = [
            {"key": "login_frequency", "label": "Login frequency", "value": round(login_freq, 2), "display": f"{int(login_freq*100)}% vs 30d"},
            {"key": "support_tickets", "label": "Support tickets", "value": round(tickets_count / 8.0, 2), "display": f"{tickets_count} open"},
            {"key": "sentiment_score", "label": "Sentiment score", "value": sentiment, "display": f"{sentiment:.2f}"},
            {"key": "feature_adoption", "label": "Feature adoption", "value": feature_adopt, "display": f"{int(feature_adopt*100)}%"},
            {"key": "billing_anomaly", "label": "Billing anomaly", "value": float(billing_flag), "display": "flagged" if billing_flag else "clean"},
            {"key": "onboarding_progress", "label": "Onboarding progress", "value": round(onboarding_steps / 6.0, 2), "display": f"{onboarding_steps}/6 steps"},
        ]

        avatar_hue = (i * 37) % 360
        joined_days = max(20, tenure_months * 30)
        last_active = max(1, int(risk_score * 12))

        customers.append({
            "id": cid,
            "name": name,
            "company": company,
            "email": email,
            "tier": tier,
            "plan_value": plan_value,
            "avatar_hue": avatar_hue,
            "joined_days": joined_days,
            "last_active_days": last_active,
            "signals": signals,
            "risk_score": risk_score,
            "risk_band": risk_band,
            "telco_meta": telco_input,
        })

    return customers


def generate_sample_outcomes(customers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Generates 28 realistic historical retention intervention outcomes for RL training."""
    actions = ["human_handoff", "incentive", "guided_tutorial", "proactive_nudge"]
    attributions = ["Contract", "tenure", "TechSupport", "InternetService", "MonthlyCharges"]
    outcomes = []
    base_time = datetime.now(timezone.utc) - timedelta(days=45)

    for i in range(28):
        c = customers[i % len(customers)]
        action = actions[i % len(actions)]
        top_attr = attributions[i % len(attributions)]
        c_risk = c["risk_score"]

        # Realistic success probability depends on matching action to risk and root cause
        if action == "human_handoff" and c_risk >= 0.7:
            status = "success" if random.random() < 0.85 else "failure"
        elif action == "incentive" and top_attr in ["MonthlyCharges", "Contract"]:
            status = "success" if random.random() < 0.78 else "failure"
        elif action == "guided_tutorial" and top_attr in ["tenure", "TechSupport"]:
            status = "success" if random.random() < 0.82 else "failure"
        else:
            status = "success" if random.random() < 0.65 else ("pending" if i > 22 else "failure")

        created_dt = base_time + timedelta(days=int(i * 1.5))
        resolved_dt = (created_dt + timedelta(days=3)).isoformat() if status != "pending" else None

        outcomes.append({
            "id": f"out_{uuid.uuid4().hex[:8]}",
            "customer_id": c["id"],
            "customer_name": c["name"],
            "risk_score": c_risk,
            "risk_band": c["risk_band"],
            "top_attribution": top_attr,
            "selected_action": action,
            "knowledge_response": f"Retention strategy for {top_attr}: applied {action.replace('_', ' ')} protocol.",
            "confidence": round(0.82 + (random.random() * 0.15), 2),
            "outcome": status,
            "created_at": created_dt.isoformat(),
            "resolved_at": resolved_dt,
        })

    return outcomes


def seed_database(force: bool = False):
    """Populates PostgreSQL / SQLite database with 50 real scored customer accounts."""
    if force:
        print("[Database] Force flag detected. Dropping and recreating tables...")
        Base.metadata.drop_all(bind=engine)
    init_db()
    db = SessionLocal()
    try:
        count = db.query(CustomerModel).count()
        if count == 0:
            print(f"[Database] Seeding real customer database...")
            real_customers = generate_real_customer_records(count=50)


            for c in real_customers:
                cust = CustomerModel(
                    id=c["id"],
                    name=c["name"],
                    company=c["company"],
                    email=c["email"],
                    tier=c["tier"],
                    plan_value=c["plan_value"],
                    avatar_hue=c["avatar_hue"],
                    joined_days=c["joined_days"],
                    last_active_days=c["last_active_days"],
                    signals_json=json.dumps(c["signals"]),
                    risk_score=c["risk_score"],
                    risk_band=c["risk_band"],
                    created_at=utc_now_iso(),
                )
                db.add(cust)

                risk_record = RiskScoreModel(
                    customer_id=c["id"],
                    risk_score=c["risk_score"],
                    risk_band=c["risk_band"],
                    attributions_json=json.dumps([{"feature": "Contract", "impact": 0.12}, {"feature": "tenure", "impact": 0.11}]),
                    model_version="svm_rbf_v2.0",
                    created_at=utc_now_iso(),
                )
                db.add(risk_record)

            # Seed historical intervention outcomes
            outcomes = generate_sample_outcomes(real_customers)
            for o in outcomes:
                db.add(OutcomeModel(**o))

            db.commit()
            print(f"[Database] Successfully seeded {len(real_customers)} customer accounts and {len(outcomes)} historical outcomes.")
            return real_customers
        else:
            print(f"[Database] Found {count} existing customer records in database. No seed required.")
            return None
    finally:
        db.close()


def sync_to_frontend_customers():
    """Generates static TypeScript array in src/lib/customers.ts to match database records."""
    db = SessionLocal()
    try:
        db_custs = db.query(CustomerModel).all()
        if not db_custs:
            print("[Database Sync] No customers in DB to sync.")
            return

        ts_items = []
        for c in db_custs:
            signals = json.loads(c.signals_json)
            ts_items.append({
                "id": c.id,
                "name": c.name,
                "company": c.company,
                "email": c.email,
                "tier": c.tier,
                "plan_value": c.plan_value,
                "avatarHue": c.avatar_hue,
                "signals": signals,
                "joinedDays": c.joined_days,
                "lastActiveDays": c.last_active_days,
            })

        customers_ts_path = BASE_DIR / "src" / "lib" / "customers.ts"
        content = f"""import type {{ Customer, CustomerSignal }} from './types';
import {{ API_BASE }} from './apiConfig';

// 50 Real Scored Customer Accounts seeded from Database and SVM Churn Model
export const customers: Customer[] = {json.dumps(ts_items, indent=2)};

export let liveCustomersCache: Customer[] = [...customers];

export async function fetchCustomers(): Promise<Customer[]> {{
  try {{
    const res = await fetch(`${{API_BASE}}/api/customers`);
    if (!res.ok) throw new Error(`HTTP ${{res.status}}`);
    const data = await res.json();
    if (Array.isArray(data) && data.length > 0) {{
      liveCustomersCache = data.map((c: any) => ({{
        id: c.id,
        name: c.name,
        company: c.company,
        email: c.email,
        tier: c.tier,
        plan_value: c.plan_value,
        avatarHue: c.avatarHue ?? c.avatar_hue ?? 180,
        signals: c.signals ?? [],
        joinedDays: c.joinedDays ?? c.joined_days ?? 30,
        lastActiveDays: c.lastActiveDays ?? c.last_active_days ?? 1,
      }}));
      return liveCustomersCache;
    }}
  }} catch (err) {{
    console.warn("Notice: Fetching customers from DB failed, using local cache:", err);
  }}
  return customers;
}}

export function findCustomer(id: string): Customer | undefined {{
  return liveCustomersCache.find((c) => c.id === id) || customers.find((c) => c.id === id);
}}
"""
        with open(customers_ts_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[Database Sync] Updated {customers_ts_path} with {len(ts_items)} real customer accounts.")
    finally:
        db.close()


if __name__ == "__main__":
    force_flag = "--force" in sys.argv
    seed_database(force=force_flag)
    sync_to_frontend_customers()
