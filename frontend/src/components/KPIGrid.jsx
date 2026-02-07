import React from 'react';
import { clsx } from 'clsx';

const KPICard = ({ kpi }) => {
    const { name, value, score_normalized, explanation, confidence_score } = kpi;

    // Color scale based on score (0-100)
    const getBarColor = (s) => {
        if (s >= 80) return 'bg-green-500';
        if (s >= 50) return 'bg-yellow-400';
        return 'bg-red-400';
    };

    return (
        <div className="bg-white p-4 rounded-lg border border-slate-200 shadow-sm hover:shadow-md transition-shadow">
            <div className="flex justify-between items-start mb-2">
                <h4 className="text-xs font-semibold text-slate-500 uppercase max-w-[70%] text-ellipsis overflow-hidden whitespace-nowrap" title={kpi.kpi_id}>
                    {kpi.kpi_id.replace(/_/g, ' ')}
                </h4>
                <span className="text-xs font-mono text-slate-400 bg-slate-100 px-1 rounded">
                    {(confidence_score * 100).toFixed(0)}% Conf.
                </span>
            </div>

            <div className="text-lg font-bold text-slate-900 mb-3 truncate">
                {value}
            </div>

            {/* Visual Bar */}
            <div className="w-full bg-slate-100 h-1.5 rounded-full mb-3 overflow-hidden">
                <div
                    className={clsx("h-full transition-all duration-500", getBarColor(score_normalized))}
                    style={{ width: `${score_normalized}%` }}
                />
            </div>

            <p className="text-xs text-slate-600 leading-snug line-clamp-3">
                {explanation}
            </p>
        </div>
    );
};

const KPIGrid = ({ kpis }) => {
    return (
        <div className="mb-8">
            <h3 className="text-lg font-semibold text-slate-800 mb-4 px-1">Key Performance Indicators</h3>
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                {kpis.map((kpi, idx) => (
                    <KPICard key={idx} kpi={kpi} />
                ))}
            </div>
        </div>
    );
};

export default KPIGrid;
