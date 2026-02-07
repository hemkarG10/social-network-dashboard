import React from 'react';
import { TrendingUp, AlertTriangle, CheckCircle, XCircle } from 'lucide-react';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

const ExecutiveSummary = ({ decisionSummary }) => {
    const { decision, roi_prediction, risk_level, executive_summary } = decisionSummary;

    const getDecisionColor = (d) => {
        if (d === 'GO') return 'bg-green-100 text-green-800 border-green-200';
        if (d === 'NO-GO') return 'bg-red-100 text-red-800 border-red-200';
        return 'bg-yellow-100 text-yellow-800 border-yellow-200';
    };

    const getRiskColor = (r) => {
        if (r === 'LOW') return 'text-green-600';
        if (r === 'MEDIUM') return 'text-yellow-600';
        return 'text-red-600';
    };

    const DecisionIcon = decision === 'GO' ? CheckCircle : (decision === 'NO-GO' ? XCircle : AlertTriangle);

    return (
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6 mb-6">
            <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-6 gap-4">
                <div>
                    <h2 className="text-sm font-semibold text-slate-500 uppercase tracking-wide">Executive Decision</h2>
                    <div className={twMerge("mt-2 px-4 py-2 rounded-lg border-2 text-2xl font-bold inline-flex items-center gap-2", getDecisionColor(decision))}>
                        <DecisionIcon size={28} />
                        {decision}
                    </div>
                </div>

                <div className="flex gap-8">
                    <div className="text-right">
                        <p className="text-sm font-medium text-slate-500">Projected ROI</p>
                        <div className="text-2xl font-bold text-slate-900 flex items-center gap-1 justify-end">
                            {roi_prediction.min}x - {roi_prediction.max}x
                            <TrendingUp size={20} className="text-green-500" />
                        </div>
                        <p className="text-xs text-slate-400">Confidence: {(roi_prediction.confidence * 100).toFixed(0)}%</p>
                    </div>

                    <div className="text-right border-l pl-8 border-slate-100">
                        <p className="text-sm font-medium text-slate-500">Risk Profile</p>
                        <div className={twMerge("text-2xl font-bold", getRiskColor(risk_level))}>
                            {risk_level}
                        </div>
                    </div>
                </div>
            </div>

            <div className="bg-slate-50 p-4 rounded-lg border border-slate-100">
                <h3 className="font-semibold text-slate-900 mb-1 flex items-center gap-2">
                    AI Summary
                </h3>
                <p className="text-slate-600 leading-relaxed">
                    {executive_summary}
                </p>
            </div>
        </div>
    );
};

export default ExecutiveSummary;
