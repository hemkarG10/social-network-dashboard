import React, { useState } from 'react';
import { Search, Sparkles, LayoutDashboard, Loader2, Bot, Layout, MessageSquare } from 'lucide-react';
import { api } from './services/api';
import ExecutiveSummary from './components/ExecutiveSummary';
import KPIGrid from './components/KPIGrid';
import AIAnalystPanel from './components/AIAnalystPanel';
import ChatPanel from './components/ChatPanel';
import LandingPage from './components/LandingPage';

function App() {
  const [view, setView] = useState('landing'); // 'landing' | 'dashboard'
  const [activeTab, setActiveTab] = useState('overview'); // 'overview' | 'chat'

  // Global Filters
  const [dateFilter, setDateFilter] = useState('1m'); // '1m' | '3m' | '6m'
  const [contentTypeFilter, setContentTypeFilter] = useState('all'); // 'all' | 'short' | 'video' | 'long'

  const [influencerId, setInfluencerId] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleEvaluate = async (e) => {
    if (e && typeof e.preventDefault === 'function') {
      e.preventDefault();
    }
    if (!influencerId.trim()) return;

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await api.evaluateDemo(influencerId, null, dateFilter, contentTypeFilter);
      setResult(data);
      setView('dashboard');
      setActiveTab('overview');
    } catch (err) {
      setError("Failed to evaluate influencer. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleSelectFromLanding = (id) => {
    setInfluencerId(id);
    // Trigger evaluation immediately but we need to wait for state update in a real app
    // Here we just call the function directly with the ID, but we need to update state too
    // Ideally useEffect but let's just hack it for MVP
    // We'll just call api directly
    setLoading(true);
    api.evaluateDemo(id, null, dateFilter, contentTypeFilter).then(data => {
      setResult(data);
      setView('dashboard');
      setActiveTab('overview');
    }).catch(() => setError("Failed")).finally(() => setLoading(false));
  };

  const goHome = () => {
    setView('landing');
    setResult(null);
    setInfluencerId('');
  };

  return (
    <div className="min-h-screen bg-slate-50 font-sans text-slate-900 pb-20">
      {/* Header */}
      <header className="bg-white border-b border-slate-200 sticky top-0 z-10">
        <div className="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
          <div onClick={goHome} className="flex items-center gap-2 text-indigo-600 font-bold text-xl cursor-pointer">
            <Sparkles size={24} />
            AI Influencer Audit
          </div>

          <form onSubmit={handleEvaluate} className="flex gap-2 w-full max-w-2xl">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={18} />
              <input
                type="text"
                value={influencerId}
                onChange={(e) => setInfluencerId(e.target.value)}
                placeholder="Enter Influencer Handle..."
                className="w-full pl-10 pr-4 py-2 rounded-lg border border-slate-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent text-sm bg-slate-50"
              />
            </div>

            <select
              value={dateFilter}
              onChange={(e) => setDateFilter(e.target.value)}
              className="bg-slate-50 border border-slate-300 text-slate-700 text-sm rounded-lg focus:ring-indigo-500 focus:border-indigo-500 block p-2 cursor-pointer"
            >
              <option value="1m">1 Month</option>
              <option value="3m">3 Months</option>
              <option value="6m">6 Months</option>
            </select>

            <select
              value={contentTypeFilter}
              onChange={(e) => setContentTypeFilter(e.target.value)}
              className="bg-slate-50 border border-slate-300 text-slate-700 text-sm rounded-lg focus:ring-indigo-500 focus:border-indigo-500 block p-2 cursor-pointer"
            >
              <option value="all">All Content</option>
              <option value="short">Short Form</option>
              <option value="long">Longform</option>
            </select>

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

        {view === 'landing' && (
          <LandingPage onSelectInfluencer={handleSelectFromLanding} />
        )}

        {view === 'dashboard' && result && (
          <div className="animate-fade-in">
            {/* Header Info */}
            <div className="mb-6 flex items-baseline justify-between">
              <div className="flex items-baseline gap-4">
                <h1 className="text-3xl font-bold text-slate-900">Audit Report</h1>
                <span className="text-slate-500 font-mono text-sm bg-white px-2 py-1 rounded border border-slate-200">ID: {result.influencer_id}</span>
              </div>
              <button className="bg-white text-indigo-600 px-4 py-2 rounded-lg text-sm font-semibold border border-indigo-200 hover:bg-indigo-50 hover:border-indigo-300 transition-colors shadow-sm">
                Reach Out
              </button>
            </div>

            {/* Tabs */}
            <div className="flex gap-4 border-b border-slate-200 mb-8">
              <button
                onClick={() => setActiveTab('overview')}
                className={`pb-3 px-1 flex items-center gap-2 font-medium transition-colors border-b-2 ${activeTab === 'overview' ? 'border-indigo-600 text-indigo-600' : 'border-transparent text-slate-500 hover:text-slate-700'}`}
              >
                <Layout size={18} /> Overview
              </button>
              <button
                onClick={() => setActiveTab('chat')}
                className={`pb-3 px-1 flex items-center gap-2 font-medium transition-colors border-b-2 ${activeTab === 'chat' ? 'border-indigo-600 text-indigo-600' : 'border-transparent text-slate-500 hover:text-slate-700'}`}
              >
                <MessageSquare size={18} /> Assistant & Deep Dive
              </button>
            </div>

            {activeTab === 'overview' ? (
              <div className="space-y-8">
                <ExecutiveSummary decisionSummary={result.decision_summary} />
                <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
                  <h3 className="font-bold text-lg mb-4 text-slate-800">Key Business Metrics</h3>
                  {/* We use specific KPIs for the overview as requested */}
                  <KPIGrid kpis={result.kpis.filter(k =>
                    ['avg_percentage_viewed', 'predicted_saves', 'promo_code_redemptions', 'predicted_shares', 'avg_view_duration', 'stayed_vs_swiped', 'comment_sentiment_quality', 'predicted_impressions'].includes(k.kpi_id)
                  )} />
                </div>
                <AIAnalystPanel kpis={result.kpis} />
              </div>
            ) : (
              <div className="grid lg:grid-cols-2 gap-8 h-[600px]">
                <div className="overflow-y-auto pr-2 space-y-6">
                  <h3 className="font-bold text-slate-700">All Performance Metrics</h3>
                  {/* Show ALL KPIs in Chat Tab for context */}
                  <KPIGrid kpis={result.kpis} compact={true} />
                </div>
                <div className="relative h-full bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
                  {/* Embedding Chat Panel directly */}
                  <div className="h-full">
                    <ChatPanel
                      influencerId={result.influencer_id}
                      isOpen={true}
                      onClose={() => { }}
                      isEmbedded={true}
                    />
                  </div>
                </div>
              </div>
            )}
          </div>
        )}

        {view === 'dashboard' && error && (
          <div className="bg-red-50 text-red-700 p-4 rounded-lg border border-red-200 mb-8 text-center">{error}</div>
        )}

      </main>
    </div>
  );
}

export default App;
