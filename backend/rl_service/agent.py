import os
import json
import numpy as np
from pathlib import Path
from typing import List, Dict, Any, Tuple

ACTIONS = ["guided_tutorial", "proactive_nudge", "human_handoff", "incentive"]

ACTION_LABELS = {
    "guided_tutorial": "Guided tutorial",
    "proactive_nudge": "Proactive nudge",
    "human_handoff": "Human handoff",
    "incentive": "Incentive",
}


class ContextualBanditAgent:
    """
    Production Contextual Bandit (LinUCB) Reinforcement Learning Agent.
    Learns state-dependent retention action values from real customer outcomes.
    """

    def __init__(self, actions: List[str] = None, alpha: float = 0.8, d: int = 8):
        self.actions = actions or ACTIONS
        self.n_actions = len(self.actions)
        self.alpha = alpha
        self.d = d

        # LinUCB parameters
        self.A = {a: np.identity(self.d, dtype=np.float64) for a in self.actions}
        self.b = {a: np.zeros((self.d, 1), dtype=np.float64) for a in self.actions}
        self.total_updates = 0
        self.history = []

    def extract_features(
        self,
        risk_score: float,
        risk_band: str,
        top_attribution: str,
        confidence: float = 0.85,
    ) -> np.ndarray:
        """
        Maps risk score, risk band, top attribution driver, and knowledge confidence
        into an 8-dimensional state context vector.
        """
        r_score = float(risk_score)
        is_crit = 1.0 if (risk_band == "critical" or r_score >= 0.75) else 0.0
        is_high = 1.0 if (risk_band == "high" or 0.55 <= r_score < 0.75) else 0.0

        top_attr = str(top_attribution).strip()
        is_pricing = 1.0 if any(k in top_attr for k in ["Contract", "pricing", "Monthly", "Total", "billing", "Payment"]) else 0.0
        is_onboarding = 1.0 if any(k in top_attr for k in ["tenure", "onboard", "usage", "dropout", "active"]) else 0.0
        is_support = 1.0 if any(k in top_attr for k in ["TechSupport", "support", "ticket", "failure", "sentiment", "Internet"]) else 0.0

        conf = float(confidence)
        bias = 1.0

        return np.array([
            r_score,
            is_crit,
            is_high,
            is_pricing,
            is_onboarding,
            is_support,
            conf,
            bias,
        ], dtype=np.float64).reshape(-1, 1)

    def predict_action_scores(
        self,
        context_vector: np.ndarray,
        temperature: float = 0.5,
    ) -> Tuple[str, List[Dict[str, Any]]]:
        """
        Computes expected rewards, exploration bounds, and softmax probabilities for all actions.
        Returns: (selected_action, [ {action, score, rationale, expected_reward}, ... ])
        """
        ucb_values = {}
        means = {}

        for a in self.actions:
            A_inv = np.linalg.pinv(self.A[a])
            theta = A_inv.dot(self.b[a])
            mean = float(theta.T.dot(context_vector)[0, 0])
            cb = float(self.alpha * np.sqrt(context_vector.T.dot(A_inv).dot(context_vector))[0, 0])
            means[a] = mean
            ucb_values[a] = mean + cb

        # Softmax probability transformation over UCB values
        max_val = max(ucb_values.values())
        exp_vals = {a: np.exp((ucb_values[a] - max_val) / temperature) for a in self.actions}
        sum_exp = sum(exp_vals.values())
        probs = {a: exp_vals[a] / sum_exp for a in self.actions}

        ranked_actions = sorted(self.actions, key=lambda a: ucb_values[a], reverse=True)
        selected_action = ranked_actions[0]

        action_scores = []
        for a in ranked_actions:
            prob = float(probs[a])
            mean_r = float(means[a])
            rationale = self._generate_rationale(a, a == selected_action, mean_r)
            action_scores.append({
                "action": a,
                "score": round(prob, 3),
                "rationale": rationale,
            })

        return selected_action, action_scores

    def _generate_rationale(self, action: str, is_top: bool, mean_reward: float) -> str:
        label = ACTION_LABELS.get(action, action)
        if is_top:
            if action == "human_handoff":
                return "Highest expected value; customer risk profile requires direct executive intervention to prevent churn."
            elif action == "incentive":
                return "Optimal policy choice; pricing sensitivity signals a high return on financial retention credits."
            elif action == "guided_tutorial":
                return "Highest expected value; addresses feature friction with contextual walkthroughs to drive user adoption."
            else:
                return "Optimal proactive retention check-in; highest EV for mild sentiment or engagement drops."
        else:
            return f"Lower expected value than top action (estimated EV: {mean_reward:+.2f})."

    def update(self, action: str, context_vector: np.ndarray, reward: float) -> None:
        """Online updates of covariance matrix A and reward vector b."""
        if action in self.actions:
            x = context_vector.reshape(-1, 1)
            self.A[action] += x.dot(x.T)
            self.b[action] += float(reward) * x
            self.total_updates += 1

    def train_from_outcomes(self, outcomes: List[Any]) -> Dict[str, Any]:
        """Retrains the bandit agent on historical database outcome records."""
        # Reset to base identity
        self.A = {a: np.identity(self.d, dtype=np.float64) for a in self.actions}
        self.b = {a: np.zeros((self.d, 1), dtype=np.float64) for a in self.actions}
        self.total_updates = 0

        trained_count = 0
        success_count = 0

        for o in outcomes:
            status = getattr(o, "outcome", None) or (o.get("outcome") if isinstance(o, dict) else None)
            if status in ["success", "failure"]:
                action = getattr(o, "selected_action", None) or (o.get("selected_action") if isinstance(o, dict) else None)
                risk_score = getattr(o, "risk_score", 0.5) or (o.get("risk_score", 0.5) if isinstance(o, dict) else 0.5)
                risk_band = getattr(o, "risk_band", "moderate") or (o.get("risk_band", "moderate") if isinstance(o, dict) else "moderate")
                top_attr = getattr(o, "top_attribution", "Contract") or (o.get("top_attribution", "Contract") if isinstance(o, dict) else "Contract")
                conf = getattr(o, "confidence", 0.85) or (o.get("confidence", 0.85) if isinstance(o, dict) else 0.85)

                reward = 1.0 if status == "success" else -0.8
                x = self.extract_features(risk_score, risk_band, top_attr, conf)
                self.update(action, x, reward)
                trained_count += 1
                if status == "success":
                    success_count += 1

        win_rate = (success_count / trained_count) if trained_count > 0 else 0.0
        return {
            "trained_samples": trained_count,
            "success_count": success_count,
            "win_rate": round(win_rate, 4),
            "total_updates": self.total_updates,
        }
