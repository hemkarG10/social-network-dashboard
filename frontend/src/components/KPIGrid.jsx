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
        <div className="bg-white p-4 rounded-lg border border-slate-200 shadow-sm hover:shadow-md transition-shadow h-full flex flex-col relative overflow-hidden">
            {/* Header: Title */}
            <div className="mb-2 pr-12">
                <h4 className="text-xs font-bold text-slate-500 uppercase tracking-wider leading-tight">
                    {kpi.kpi_id.replace(/_/g, ' ')}
                </h4>
            </div>

            {/* Value */}
            <div className="text-2xl font-bold text-slate-900 mb-3">
                {value}
            </div>

            {/* Visual Bar */}
            <div className="w-full bg-slate-100 h-1.5 rounded-full mb-3 overflow-hidden">
                <div
                    className={clsx("h-full transition-all duration-500", getBarColor(score_normalized))}
                    style={{ width: `${score_normalized}%` }}
                />
            </div>

            {/* Explanation - Grows to fill space, no clamp */}
            <p className="text-xs text-slate-600 leading-relaxed flex-grow">
                {explanation}
            </p>

            {/* Confidence Badge with Tooltip */}
            <div className="absolute top-4 right-4 group">
                <span
                    className={clsx(
                        "text-[10px] font-mono px-1.5 py-0.5 rounded border opacity-80 cursor-help",
                        confidence_score > 0.8 ? "bg-green-50 text-green-700 border-green-200" :
                            confidence_score > 0.5 ? "bg-yellow-50 text-yellow-700 border-yellow-200" :
                                "bg-slate-50 text-slate-500 border-slate-200"
                    )}
                >
                    {Math.round(confidence_score * 100)}%
                </span>

                {/* Tooltip */}
                <div className="hidden group-hover:block absolute right-0 top-6 z-10 w-48 p-2 bg-slate-800 text-white text-[10px] rounded shadow-lg border border-slate-700 leading-tight">
                    <strong>Confidence Score</strong>
                    <br />
                    Indicates AI certainty based on data pattern consistency and historical accuracy.
                </div>
            </div>
        </div>
    );
};

const KPIGrid = ({ kpis, compact = false, onKpiClick }) => {
    return (
        <div className={compact ? "" : "mb-8"}>
            <div className={`grid gap-4 ${compact ? 'grid-cols-1' : 'grid-cols-2 md:grid-cols-3 lg:grid-cols-5'}`}>
                {kpis.map((kpi, idx) => (
                    <div key={idx} onClick={() => onKpiClick && onKpiClick(kpi)} className={onKpiClick ? "cursor-pointer" : ""}>
                        <KPICard kpi={kpi} />
                    </div>
                ))}
            </div>
        </div>
    );
};

export default KPIGrid;
