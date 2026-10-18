import { useState, lazy, Suspense } from 'react';
import { Sidebar, MobileNav, type ViewKey } from '@/components/layout/Sidebar';
import { Topbar } from '@/components/layout/Topbar';
import { DashboardView } from '@/components/views/DashboardView';

const ThinkView = lazy(() => import('@/components/views/ThinkView').then(m => ({ default: m.ThinkView })));
const CustomersView = lazy(() => import('@/components/views/CustomersView').then(m => ({ default: m.CustomersView })));
const OutcomesView = lazy(() => import('@/components/views/OutcomesView').then(m => ({ default: m.OutcomesView })));
const HealthView = lazy(() => import('@/components/views/HealthView').then(m => ({ default: m.HealthView })));
const NeuralView = lazy(() => import('@/components/views/NeuralView').then(m => ({ default: m.NeuralView })));
const ReinforcementView = lazy(() => import('@/components/views/ReinforcementView').then(m => ({ default: m.ReinforcementView })));

function ViewFallback() {
  return (
    <div className="flex flex-1 items-center justify-center p-12">
      <div className="flex items-center gap-3 rounded-2xl border border-white/5 bg-[#0f1722]/60 px-5 py-3 backdrop-blur-xl shadow-lg">
        <div className="h-4 w-4 animate-spin rounded-full border-2 border-cyan-400 border-t-transparent" />
        <span className="text-sm font-medium text-slate-300">Loading view...</span>
      </div>
    </div>
  );
}

const META: Record<ViewKey, { title: string; subtitle: string }> = {
  dashboard: { title: 'Overview', subtitle: 'Customer intelligence across your book of business' },
  think: { title: 'See the AI Think', subtitle: 'Watch the orchestrator reason across three subsystems' },
  customers: { title: 'Customers', subtitle: 'Every account, scored for churn risk and explained' },
  outcomes: { title: 'Feedback Loop', subtitle: 'Outcomes, root-cause aggregation, and policy retraining' },
  health: { title: 'System Health', subtitle: 'Subsystem status, endpoints, and live connectivity' },
  neural: { title: 'Neural Network', subtitle: 'Neural network policy visualization' },
  reinforcement: { title: 'Reinforcement Learning', subtitle: 'Learned from 2,400 past interventions' },
};

function App() {
  const [view, setView] = useState<ViewKey>('dashboard');
  const [analyzeId, setAnalyzeId] = useState<string | undefined>(undefined);
  const [busy] = useState(false);

  function navigate(v: ViewKey) {
    setView(v);
  }

  function analyzeCustomer(id: string) {
    setAnalyzeId(id);
    setView('think');
  }

  const meta = META[view];

  return (
    <div className="flex min-h-screen w-full bg-[#04070d] text-slate-200">
      {/* Ambient background glow */}
      <div className="pointer-events-none fixed inset-0 z-0 overflow-hidden">
        <div className="absolute left-1/4 -top-32 h-[500px] w-[700px] rounded-full bg-cyan-600/20 blur-[140px] mix-blend-screen animate-pulseGlow" />
        <div className="absolute -bottom-32 right-1/4 h-[400px] w-[600px] rounded-full bg-violet-600/20 blur-[120px] mix-blend-screen" />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 h-[800px] w-[1200px] rounded-full bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-cyan-900/10 via-[#04070d]/0 to-transparent blur-[100px]" />
      </div>

      <Sidebar view={view} onNavigate={navigate} />

      <div className="relative z-10 flex min-w-0 flex-1 flex-col">
        <MobileNav view={view} onNavigate={navigate} />
        <div className="w-full flex-1 flex flex-col px-4 py-6 sm:px-6 lg:px-8">
          <Topbar title={meta.title} subtitle={meta.subtitle} busy={busy} />
          <main className="mt-6 flex-1 flex flex-col">
            <Suspense fallback={<ViewFallback />}>
              {view === 'dashboard' && <DashboardView onNavigate={navigate} />}
              {view === 'think' && <ThinkView initialCustomerId={analyzeId} />}
              {view === 'customers' && (
                <CustomersView onAnalyze={analyzeCustomer} />
              )}
              {view === 'outcomes' && <OutcomesView />}
              {view === 'health' && <HealthView />}
              {view === 'neural' && <NeuralView />}
              {view === 'reinforcement' && <ReinforcementView />}
            </Suspense>
          </main>
        </div>
      </div>
    </div>
  );
}

export default App;
