import React, { useState } from 'react';
import { Search, Sparkles, LayoutDashboard, Loader2 } from 'lucide-react';
import { api } from './services/api';
import ExecutiveSummary from './components/ExecutiveSummary';
import KPIGrid from './components/KPIGrid';
import AIAnalystPanel from './components/AIAnalystPanel';

function App() {
  const [influencerId, setInfluencerId] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleEvaluate = async (e) => {
    e.preventDefault();
    if (!influencerId.trim()) return;

    setLoading(true);
    setError(null);
    try {
      const data = await api.evaluateDemo(influencerId);
      setResult(data);
    } catch (err) {
      setError("Failed to evaluate influencer. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 font-sans text-slate-900 pb-20">
      {/* Header */}
      <header className="bg-white border-b border-slate-200 sticky top-0 z-10">
        <div className="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2 text-indigo-600 font-bold text-xl">
            <Sparkles size={24} />
            AI Influencer Audit
          </div>

          <form onSubmit={handleEvaluate} className="flex gap-2 w-full max-w-md">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={18} />
              <input
                type="text"
                value={influencerId}
                onChange={(e) => setInfluencerId(e.target.value)}
                placeholder="Enter Influencer Handle or ID..."
                className="w-full pl-10 pr-4 py-2 rounded-lg border border-slate-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent text-sm bg-slate-50"
              />
            </div>
            <button
              type="submit"
              disabled={loading}
              className="bg-indigo-600 text-white px-4 py-2 rounded-lg text-sm font-semibold hover:bg-indigo-700 transition-colors disabled:opacity-50 flex items-center gap-2"
            >
              {loading ? <Loader2 size={16} className="animate-spin" /> : 'Evaluate'}
            </button>
          </form>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-6xl mx-auto px-4 py-8">
        {!result && !loading && !error && (
          <div className="text-center py-20">
            <div className="bg-white p-8 rounded-2xl shadow-sm border border-slate-200 inline-block max-w-lg">
              <div className="w-16 h-16 bg-indigo-50 text-indigo-600 rounded-full flex items-center justify-center mx-auto mb-4">
                <LayoutDashboard size={32} />
              </div>
              <h1 className="text-2xl font-bold text-slate-800 mb-2">Ready to Audit</h1>
              <p className="text-slate-500">
                Enter an influencer ID to generate a real-time, AI-driven audit.
                Our system uses synthetic data to simulate 14+ KPIs and provide a decision-grade analysis.
              </p>
              <div className="mt-6 flex flex-wrap gap-2 justify-center">
                <button onClick={() => setInfluencerId('tech-guru-99')} className="text-xs bg-slate-100 hover:bg-slate-200 px-3 py-1 rounded-full text-slate-600">Try "tech-guru-99"</button>
                <button onClick={() => setInfluencerId('fashion-star-1')} className="text-xs bg-slate-100 hover:bg-slate-200 px-3 py-1 rounded-full text-slate-600">Try "fashion-star-1"</button>
              </div>
            </div>
          </div>
        )}

        {error && (
          <div className="bg-red-50 text-red-700 p-4 rounded-lg border border-red-200 mb-8 text-center">
            {error}
          </div>
        )}

        {result && (
          <div className="animate-fade-in">
            <div className="mb-6 flex items-baseline gap-4">
              <h1 className="text-3xl font-bold text-slate-900">Audit Report</h1>
              <span className="text-slate-500 font-mono text-sm bg-white px-2 py-1 rounded border border-slate-200">ID: {result.influencer_id}</span>
            </div>

            <ExecutiveSummary decisionSummary={result.decision_summary} />
            <KPIGrid kpis={result.kpis} />
            <AIAnalystPanel kpis={result.kpis} />
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
