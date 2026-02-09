import React from 'react';
import { ShieldAlert, BarChart3, Users } from 'lucide-react';
import { clsx } from 'clsx';

const AnalystCard = ({ role, icon: Icon, color, kpis }) => {
    return (
        <div className="border border-slate-200 rounded-lg bg-white overflow-hidden shadow-sm h-full flex flex-col">
            <div className="w-full flex items-center justify-between p-4 bg-slate-50 border-b border-slate-100">
                <div className="flex items-center gap-3">
                    <div className={clsx("p-2 rounded-lg", color)}>
                        <Icon size={20} className="text-white" />
                    </div>
                    <div className="flex flex-col">
                        <h4 className="font-semibold text-slate-800">{role}</h4>
                        <span className="text-xs text-slate-500 font-medium">{kpis.length} Metrics Analyzed</span>
                    </div>
                </div>
            </div>

            <div className="p-4 space-y-3 bg-white flex-1 overflow-y-auto max-h-[400px]">
                {kpis.map((kpi, idx) => (
                    <div key={idx} className="border-b last:border-0 border-slate-50 pb-3 last:pb-0">
                        <div className="flex justify-between items-baseline mb-1">
                            <span className="text-xs font-semibold text-slate-600 uppercase tracking-wide">
                                {kpi.kpi_id.replace(/_/g, ' ')}
                            </span>
                            <span className="font-bold text-slate-900 font-mono">{kpi.value}</span>
                        </div>
                        <p className="text-sm text-slate-600 bg-slate-50 p-2 rounded-md italic leading-relaxed border border-slate-100">
                            "{kpi.explanation}"
                        </p>
                    </div>
                ))}
            </div>
        </div>
    );
};

// Helper function to categorize KPIs
const categorize = (kpi) => {
    const id = kpi.kpi_id;
    // Categorization logic based on ID patterns
    if (id.includes('brand_safety') || id.includes('brand_readiness') || id.includes('controversy') || id.includes('fake_follower') || id.includes('platform_risk')) return 'risk';
    if (id.includes('authenticity') || id.includes('engagement_quality') || id.includes('audience') || id.includes('fatigue') || id.includes('sentiment') || id.includes('loyalty') || id.includes('credibility')) return 'audience';
    // Default to performance for everything else (impressions, views, etc)
    return 'performance';
};

const AIAnalystPanel = ({ kpis }) => {
    if (!kpis) return null;

    const performanceKPIs = kpis.filter(k => categorize(k) === 'performance');
    const riskKPIs = kpis.filter(k => categorize(k) === 'risk');
    const audienceKPIs = kpis.filter(k => categorize(k) === 'audience');

    return (
        <div className="mb-8">
            <h3 className="text-lg font-semibold text-slate-800 mb-4 px-1">AI Staff Analysis</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <AnalystCard
                    role="Performance Analyst"
                    icon={BarChart3}
                    color="bg-blue-500"
                    kpis={performanceKPIs}
                />
                <AnalystCard
                    role="Risk Analyst"
                    icon={ShieldAlert}
                    color="bg-red-500"
                    kpis={riskKPIs}
                />
                <AnalystCard
                    role="Audience Strategist"
                    icon={Users}
                    color="bg-purple-500"
                    kpis={audienceKPIs}
                />
            </div>
        </div>
    );
};

export default AIAnalystPanel;
