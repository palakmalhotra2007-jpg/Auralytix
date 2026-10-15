import type { Connect } from 'vite';

interface ActionScore {
  action: string;
  score: number;
  rationale: string;
}

const POLICY_RULES: Record<string, { action: string; rationale: string }> = {
  onboarding_confusion: {
    action: 'guided_tutorial',
    rationale: 'Onboarding confusion is best resolved by a guided tutorial that walks the user to their first win.',
  },
  repeated_failures: {
    action: 'human_handoff',
    rationale: 'Repeated failures typically stem from integration misconfigurations that a live session resolves far more often than an async nudge.',
  },
  pricing_concern: {
    action: 'incentive',
    rationale: 'Pricing concern signals downgrade risk; a loyalty credit gated on renewal commitment is the highest-EV move.',
  },
  sentiment_decline: {
    action: 'proactive_nudge',
    rationale: 'Sentiment decline responds to a personal CSM check-in paired with a roadmap share, not a scripted nudge.',
  },
  engagement_drop: {
    action: 'proactive_nudge',
    rationale: 'Engagement drop is addressed by a single feature-tied proactive nudge within the dormancy window.',
  },
  billing_anomaly: {
    action: 'incentive',
    rationale: 'Billing anomalies signal urgent retention risk; a tailored discount or payment restructuring stops churn.',
  },
};

const FEATURE_LABELS: Record<string, string> = {
  onboarding_confusion: 'Onboarding confusion',
  repeated_failures: 'Repeated failures',
  pricing_concern: 'Pricing concern',
  sentiment_decline: 'Sentiment decline',
  engagement_drop: 'Engagement drop',
  billing_anomaly: 'Billing anomaly',
};

const KB_ARTICLES: Record<string, { docs: { doc_id: string; title: string; snippet: string; score: number }[]; response: string }> = {
  onboarding_confusion: {
    docs: [
      { doc_id: 'KB-101', title: 'Product Onboarding & Quickstart Guide', snippet: 'Step 3 requires OAuth token generation. 42% of stalled users report UI confusion here.', score: 0.94 },
      { doc_id: 'KB-104', title: 'Interactive Product Tours Setup', snippet: 'Enabling in-app walkthrough modals boosts initial retention by 31%.', score: 0.89 },
    ],
    response: 'User exhibits stalled onboarding progression at step 3. Recommend triggering an interactive onboarding walkthrough and dispatching the technical Quickstart checklist.',
  },
  repeated_failures: {
    docs: [
      { doc_id: 'KB-208', title: 'Webhook Timeout & Rate Limit Protocols', snippet: 'Repeated 504 and 429 errors typically indicate unbatched webhook subscriptions.', score: 0.96 },
      { doc_id: 'KB-312', title: 'Tier-1 Escalation Workflows', snippet: 'Accounts encountering >3 weekly API faults should receive immediate white-glove human handoff.', score: 0.92 },
    ],
    response: 'Telemetry detects repeated integration timeouts and API failures. Recommended intervention is immediate senior technical engineer handoff and webhook payload inspection.',
  },
  pricing_concern: {
    docs: [
      { doc_id: 'KB-401', title: 'Contract Renewal & Loyalty Discount Schedules', snippet: 'Accounts flagging billing anomalies or price sensitivity are eligible for 15% annual commitment credits.', score: 0.93 },
      { doc_id: 'KB-405', title: 'Seat Optimization vs Downgrade Playbook', snippet: 'Audit inactive seat counts to restructure billing before contract churn occurs.', score: 0.88 },
    ],
    response: 'Billing signals show pricing sensitivity and downgrade inquiry. Recommended intervention is issuing a tailored loyalty credit gated on annual contract renewal.',
  },
  sentiment_decline: {
    docs: [
      { doc_id: 'KB-502', title: 'Executive Sponsor Outreach Matrix', snippet: 'Negative sentiment velocity exceeding 20% over 14 days requires CSM roadmap briefing.', score: 0.95 },
      { doc_id: 'KB-515', title: 'Feature Request Status & Escalations', snippet: 'Transparent updates on in-progress customer tickets consistently recover CSAT scores.', score: 0.90 },
    ],
    response: 'Customer sentiment metrics indicate frustration following unresolved support tickets. Recommended intervention is direct CSM executive check-in with roadmap preview.',
  },
  engagement_drop: {
    docs: [
      { doc_id: 'KB-601', title: 'Re-engagement Triggers & Feature Nudges', snippet: 'Login drops >40% in a 30-day window respond best to contextual feature-specific nudge emails.', score: 0.91 },
      { doc_id: 'KB-609', title: 'Collaboration & Team Workspace Activation', snippet: 'Inviting secondary team members increases retention durability by 2.8x.', score: 0.87 },
    ],
    response: 'Customer login frequency has declined sharply over the past 14 days. Recommended intervention is an automated proactive nudge highlighting newly shipped collaboration tools.',
  },
};

// Seed realistic outcome records
export const INITIAL_OUTCOMES = [
  {
    id: 'out_001',
    customer_id: 'c_002',
    customer_name: 'Diego Alvarez',
    risk_score: 0.78,
    risk_band: 'critical',
    top_attribution: 'repeated_failures',
    selected_action: 'human_handoff',
    knowledge_response: 'Senior engineering session scheduled to diagnose webhook timeouts.',
    confidence: 0.92,
    outcome: 'success',
    created_at: new Date(Date.now() - 3600000 * 4).toISOString(),
    resolved_at: new Date(Date.now() - 3600000 * 2).toISOString(),
  },
  {
    id: 'out_002',
    customer_id: 'c_006',
    customer_name: 'Lucas Pereira',
    risk_score: 0.84,
    risk_band: 'critical',
    top_attribution: 'billing_anomaly',
    selected_action: 'incentive',
    knowledge_response: 'Extended 15% loyalty retention credit offered on annual commitment.',
    confidence: 0.88,
    outcome: 'pending',
    created_at: new Date(Date.now() - 3600000 * 6).toISOString(),
    resolved_at: null,
  },
  {
    id: 'out_003',
    customer_id: 'c_004',
    customer_name: 'Sam Okafor',
    risk_score: 0.72,
    risk_band: 'high',
    top_attribution: 'onboarding_confusion',
    selected_action: 'guided_tutorial',
    knowledge_response: 'Interactive product walkthrough dispatched for API setup.',
    confidence: 0.94,
    outcome: 'success',
    created_at: new Date(Date.now() - 3600000 * 12).toISOString(),
    resolved_at: new Date(Date.now() - 3600000 * 9).toISOString(),
  },
  {
    id: 'out_004',
    customer_id: 'c_007',
    customer_name: 'Aaliyah Brooks',
    risk_score: 0.65,
    risk_band: 'high',
    top_attribution: 'sentiment_decline',
    selected_action: 'proactive_nudge',
    knowledge_response: 'CSM executive check-in email sent with product roadmap briefing.',
    confidence: 0.91,
    outcome: 'pending',
    created_at: new Date(Date.now() - 3600000 * 18).toISOString(),
    resolved_at: null,
  },
  {
    id: 'out_005',
    customer_id: 'c_009',
    customer_name: 'Ines Garcia',
    risk_score: 0.68,
    risk_band: 'high',
    top_attribution: 'engagement_drop',
    selected_action: 'proactive_nudge',
    knowledge_response: 'Notification sent highlighting new team collaboration workspaces.',
    confidence: 0.89,
    outcome: 'success',
    created_at: new Date(Date.now() - 3600000 * 28).toISOString(),
    resolved_at: new Date(Date.now() - 3600000 * 20).toISOString(),
  },
  {
    id: 'out_006',
    customer_id: 'c_011',
    customer_name: 'Greta Lindholm',
    risk_score: 0.58,
    risk_band: 'moderate',
    top_attribution: 'pricing_concern',
    selected_action: 'incentive',
    knowledge_response: 'Tier discount schedule shared for upcoming quarterly renewal.',
    confidence: 0.86,
    outcome: 'failure',
    created_at: new Date(Date.now() - 3600000 * 36).toISOString(),
    resolved_at: new Date(Date.now() - 3600000 * 24).toISOString(),
  },
];

let recordedOutcomes = [...INITIAL_OUTCOMES];
let policyVersion = 'policy-softmax-v1.6.0';
let isRetrained = false;
let lastRetrainedAt: string | null = null;

function json(res: any, status: number, data: any) {
  res.statusCode = status;
  res.setHeader('Content-Type', 'application/json');
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  res.end(JSON.stringify(data));
}

function readBody(req: any): Promise<any> {
  return new Promise((resolve) => {
    let body = '';
    req.on('data', (chunk: Buffer) => {
      body += chunk.toString();
    });
    req.on('end', () => {
      try {
        resolve(body ? JSON.parse(body) : {});
      } catch {
        resolve({});
      }
    });
  });
}

function computeAggregates() {
  const byAction: Record<string, { count: number; success_rate: number }> = {
    guided_tutorial: { count: 0, success_rate: 0 },
    proactive_nudge: { count: 0, success_rate: 0 },
    human_handoff: { count: 0, success_rate: 0 },
    incentive: { count: 0, success_rate: 0 },
  };

  const byRoot: Record<string, { count: number; riskSum: number }> = {};

  for (const r of recordedOutcomes) {
    if (!byAction[r.selected_action]) {
      byAction[r.selected_action] = { count: 0, success_rate: 0 };
    }
    byAction[r.selected_action].count += 1;

    const root = r.top_attribution || 'engagement_drop';
    if (!byRoot[root]) {
      byRoot[root] = { count: 0, riskSum: 0 };
    }
    byRoot[root].count += 1;
    byRoot[root].riskSum += r.risk_score || 0;
  }

  for (const act of Object.keys(byAction)) {
    const list = recordedOutcomes.filter((r) => r.selected_action === act);
    const resolved = list.filter((r) => r.outcome !== 'pending');
    const successes = resolved.filter((r) => r.outcome === 'success').length;
    byAction[act].success_rate = resolved.length ? +(successes / resolved.length).toFixed(3) : 0;
  }

  const byRootCause = Object.entries(byRoot)
    .map(([feature, val]) => ({
      feature,
      label: FEATURE_LABELS[feature] || feature.replace(/_/g, ' '),
      count: val.count,
      avg_risk: val.count ? +(val.riskSum / val.count).toFixed(3) : 0,
    }))
    .sort((a, b) => b.count - a.count);

  return {
    total: recordedOutcomes.length,
    by_action: byAction,
    by_root_cause: byRootCause,
    model_version: policyVersion,
    retrained: isRetrained,
    last_retrain: lastRetrainedAt,
  };
}

export function auralytixDevApiMiddleware(): Connect.NextHandleFunction {
  return async (req, res, next) => {
    const url = req.url?.split('?')[0] || '';
    const method = req.method || 'GET';

    if (method === 'OPTIONS') {
      res.statusCode = 204;
      res.setHeader('Access-Control-Allow-Origin', '*');
      res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE');
      res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
      res.end();
      return;
    }

    // 1. Health check
    if (url === '/health') {
      return json(res, 200, {
        status: 'ok',
        message: 'Auralytix Unified API Engine Running',
        cloud_provider: 'AWS',
        database: 'Operational',
        models: {
          risk_engine: 'PyTorch SHAP v1.0',
          knowledge_assistant: 'pulse-llm-lora-v0.9.3',
          action_policy: policyVersion
        }
      });
    }

    // 2. Customers
    if (url === '/api/customers') {
      const sampleCustomers = [
        { id: 'c_001', name: 'Maya Chen', company: 'Northwind Robotics', email: 'maya@northwind.io', tier: 'Enterprise', plan_value: 12000, avatarHue: 210, joinedDays: 45, lastActiveDays: 1, signals: [{ key: 'login_frequency', label: 'Login frequency', value: 0.85, display: '85% vs 30d' }, { key: 'support_tickets', label: 'Support tickets', value: 0.2, display: '1 open' }, { key: 'sentiment_score', label: 'Sentiment score', value: 0.82, display: '0.82' }] },
        { id: 'c_002', name: 'Diego Alvarez', company: 'Lumen Health', email: 'diego@lumenhealth.com', tier: 'Growth', plan_value: 4500, avatarHue: 160, joinedDays: 80, lastActiveDays: 3, signals: [{ key: 'login_frequency', label: 'Login frequency', value: 0.45, display: '45% vs 30d' }, { key: 'support_tickets', label: 'Support tickets', value: 0.75, display: '5 open' }, { key: 'sentiment_score', label: 'Sentiment score', value: 0.41, display: '0.41' }] },
        { id: 'c_003', name: 'Priya Nair', company: 'Atlas Freight', email: 'priya@atlasfreight.co', tier: 'Starter', plan_value: 990, avatarHue: 280, joinedDays: 20, lastActiveDays: 1, signals: [{ key: 'login_frequency', label: 'Login frequency', value: 0.9, display: '90% vs 30d' }, { key: 'support_tickets', label: 'Support tickets', value: 0.1, display: '0 open' }, { key: 'sentiment_score', label: 'Sentiment score', value: 0.95, display: '0.95' }] },
      ];
      return json(res, 200, sampleCustomers);
    }

    // 3. SHAP Risk Engine
    if (url === '/shap/risk/score') {
      const body = method === 'POST' ? await readBody(req) : {};
      const usageDecline = body.usage_decline ?? 0.4;
      const negSentiment = body.negative_sentiment ?? 0.35;
      const tickets = (body.tickets_last30 ?? 2) / 10;
      const dropout = body.feature_dropout ?? 0.4;

      const riskScore = Math.max(0.12, Math.min(0.95, (usageDecline * 0.35) + (negSentiment * 0.3) + (tickets * 0.25) + (dropout * 0.1)));

      const attributions = [
        { feature: 'repeated_failures', impact: +(tickets * 0.45).toFixed(3) },
        { feature: 'sentiment_decline', impact: +(negSentiment * 0.38).toFixed(3) },
        { feature: 'engagement_drop', impact: +(usageDecline * 0.32).toFixed(3) },
        { feature: 'onboarding_confusion', impact: +(dropout * 0.28).toFixed(3) },
        { feature: 'pricing_concern', impact: +(body.payment_delay ? 0.25 : -0.1).toFixed(3) },
      ].sort((a, b) => Math.abs(b.impact) - Math.abs(a.impact));

      return json(res, 200, {
        risk_score: +riskScore.toFixed(3),
        attributions,
        model_version: 'v1.0',
        timestamp: new Date().toISOString()
      });
    }

    // 4. RAG Knowledge Assistant
    if (url === '/rag/knowledge/respond') {
      const body = method === 'POST' ? await readBody(req) : {};
      const q = (body.issue_text || '').toLowerCase();
      let matchedKey = 'engagement_drop';
      if (q.includes('onboarding')) matchedKey = 'onboarding_confusion';
      else if (q.includes('failure') || q.includes('repeated') || q.includes('timeout')) matchedKey = 'repeated_failures';
      else if (q.includes('price') || q.includes('pricing') || q.includes('billing')) matchedKey = 'pricing_concern';
      else if (q.includes('sentiment') || q.includes('csat')) matchedKey = 'sentiment_decline';

      const entry = KB_ARTICLES[matchedKey] || KB_ARTICLES.engagement_drop;
      return json(res, 200, {
        retrieved_docs: entry.docs,
        grounded_response: entry.response,
        confidence: 0.94,
        model_version: 'pulse-llm-lora-v0.9.3'
      });
    }

    // 5. Policy Decide
    if (url === '/policy/decide') {
      const body = method === 'POST' ? await readBody(req) : {};
      const topAttr = body.top_attribution || 'engagement_drop';
      const rule = POLICY_RULES[topAttr] || { action: 'proactive_nudge', rationale: 'Default to proactive outreach.' };
      
      const scores: ActionScore[] = [
        { action: rule.action, score: 0.48, rationale: rule.rationale },
        { action: 'guided_tutorial', score: 0.22, rationale: 'Alternative onboarding support path.' },
        { action: 'proactive_nudge', score: 0.18, rationale: 'General retention engagement trigger.' },
        { action: 'human_handoff', score: 0.12, rationale: 'Escalation for high-touch accounts.' },
      ].sort((a, b) => b.score - a.score);

      return json(res, 200, {
        customer_id: body.customer_id || 'c_001',
        customer_name: body.customer_name || 'Customer',
        risk_score: body.risk_score || 0.5,
        risk_band: body.risk_band || 'moderate',
        top_attribution: topAttr,
        selected_action: rule.action,
        action_scores: scores,
        action_rationale: rule.rationale,
        knowledge_response: body.knowledge_response || 'Standard intervention plan',
        knowledge_confidence: body.knowledge_confidence || 0.9,
        model_version: policyVersion,
        decided_at: new Date().toISOString()
      });
    }

    // 6. List all outcomes (GET /policy/outcomes or GET /policy/outcome)
    if ((url === '/policy/outcomes' || url === '/policy/outcome') && method === 'GET') {
      return json(res, 200, recordedOutcomes);
    }

    // 7. Update an outcome (POST /policy/outcome/update)
    if (url === '/policy/outcome/update' && method === 'POST') {
      const body = await readBody(req);
      const outcomeId = body.id;
      const target = recordedOutcomes.find((r) => r.id === outcomeId);
      if (target) {
        target.outcome = body.outcome;
        target.resolved_at = new Date().toISOString();
        return json(res, 200, target);
      }
      return json(res, 404, { error: 'Outcome not found' });
    }

    // 8. Log a new outcome (POST /policy/outcome)
    if (url === '/policy/outcome' && method === 'POST') {
      const body = await readBody(req);
      const dec = body.decision || body;
      const newRecord = {
        id: `out_${Date.now().toString().slice(-6)}_${Math.random().toString(36).slice(2, 6)}`,
        customer_id: dec.customer_id || 'c_unknown',
        customer_name: dec.customer_name || 'Customer',
        risk_score: dec.risk_score ?? 0.5,
        risk_band: dec.risk_band || 'moderate',
        top_attribution: dec.top_attribution || 'engagement_drop',
        selected_action: dec.selected_action || 'proactive_nudge',
        knowledge_response: dec.knowledge_response || '',
        confidence: dec.knowledge_confidence ?? dec.confidence ?? 0.9,
        outcome: dec.outcome || 'pending',
        created_at: new Date().toISOString(),
        resolved_at: null,
      };
      recordedOutcomes.unshift(newRecord);
      return json(res, 200, newRecord);
    }

    // 9. Aggregate metrics (GET /policy/aggregate)
    if (url === '/policy/aggregate') {
      const aggData = computeAggregates();
      return json(res, 200, aggData);
    }

    // 10. Retrain policy model (POST /policy/retrain)
    if (url === '/policy/retrain' && method === 'POST') {
      isRetrained = true;
      lastRetrainedAt = new Date().toISOString();
      const parts = policyVersion.split('.');
      const minor = parseInt(parts[2] || '0', 10) + 1;
      policyVersion = `${parts[0]}.${parts[1]}.${minor}`;
      return json(res, 200, {
        retrained: true,
        model_version: policyVersion,
        accuracy_delta: '+2.8%',
        samples_processed: recordedOutcomes.length,
      });
    }

    // 11. RL Feedback thumbs up/down
    if (url === '/rl/feedback') {
      return json(res, 200, { status: 'recorded' });
    }

    // 12. Cloud status
    if (url === '/cloud/status') {
      return json(res, 200, {
        cloud_provider: 'AWS (Free Tier Eligible)',
        s3: { status: 'connected', bucket: 'auralytix-cloud-artifacts' },
        rds: { status: 'connected', engine: 'PostgreSQL 16' },
        status: 'healthy'
      });
    }

    return next();
  };
}
