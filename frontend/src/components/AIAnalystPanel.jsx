import React, { useState } from 'react';
import { ChevronDown, ChevronUp, User, ShieldAlert, BarChart3, Users } from 'lucide-react';
import { clsx } from 'clsx';

const AnalystCard = ({ role, icon: Icon, color, kpis }) => {
    const [isOpen, setIsOpen] = useState(true);

    return (
        <div className="border border-slate-200 rounded-lg bg-white overflow-hidden shadow-sm">
            <button
                onClick={() => setIsOpen(!isOpen)}
                className="w-full flex items-center justify-between p-4 bg-slate-50 hover:bg-slate-100 transition-colors"
            >
                <div className="flex items-center gap-3">
                    <div className={clsx("p-2 rounded-lg", color)}>
                        <Icon size={20} className="text-white" />
                    </div>
                    <h4 className="font-semibold text-slate-800">{role}</h4>
                </div>
                {isOpen ? <ChevronUp size={20} className="text-slate-400" /> : <ChevronDown size={20} className="text-slate-400" />}
            </button>

            {isOpen && (
                <div className="p-4 space-y-3 bg-white">
                    {kpis.map((kpi, idx) => (
                        <div key={idx} className="border-b last:border-0 border-slate-50 pb-2 last:pb-0">
                            <div className="flex justify-between items-baseline mb-1">
                                <span className="text-xs font-medium text-slate-500 uppercase">{kpi.kpi_id.replace(/_/g, ' ')}</span>
                                <span className="font-bold text-slate-900">{kpi.value}</span>
                            </div>
                            <p className="text-sm text-slate-600 bg-slate-50 p-2 rounded italic">
                                "{kpi.explanation}"
                            </p>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

const AIAnalystPanel = ({ kpis }) => {
    // Filter KPIs by role domain (based on ID prefixes or known lists)
    // Since the API returns a flat list, we need to bucket them.
    // In a real app, the API should group them. For MVP, we categorize by ID strings.

    const categorize = (k) => {
        const id = k.kpi_id;
        if (id.includes('brand_safety') || id.includes('controversy') || id.includes('fake_follower') || id.includes('platform_risk')) return 'risk';
        if (id.includes('authenticity') || id.includes('engagement_quality') || id.includes('audience_brand') || id.includes('fatigue')) return 'audience';
        return 'performance';
    };

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
