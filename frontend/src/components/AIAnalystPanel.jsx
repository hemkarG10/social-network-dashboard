import React, { useState } from 'react';
import { ChevronDown, ChevronUp, User, ShieldAlert, BarChart3, Users } from 'lucide-react';
import { clsx } from 'clsx';

const AnalystCard = ({ report, icon: Icon, color }) => {
    const [isOpen, setIsOpen] = useState(true);
    const { role, kpis, analysis } = report;

    return (
        <div className="border border-slate-200 rounded-lg bg-white overflow-hidden shadow-sm h-full flex flex-col">
            <button
                onClick={() => setIsOpen(!isOpen)}
                className="w-full flex items-center justify-between p-4 bg-slate-50 hover:bg-slate-100 transition-colors border-b border-slate-100"
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
                <div className="p-5 flex flex-col gap-4 text-sm flex-1">
                    {/* Headline Section */}
                    <div className="pb-3 border-b border-slate-100">
                        <div className="flex justify-between items-center mb-1">
                            <span className="font-bold text-slate-700">Analysis Headline</span>
                            <span className="text-xs font-mono bg-slate-100 px-2 py-0.5 rounded text-slate-500">{analysis.magnitude}</span>
                        </div>
                        <p className="text-slate-800 leading-snug font-medium">"{analysis.headline}"</p>
                    </div>

                    {/* Drivers & Hypotheses */}
                    <div className="grid grid-cols-1 gap-3">
                        <div>
                            <h5 className="text-xs font-bold text-slate-500 uppercase mb-1">Top Drivers (Segments)</h5>
                            <ul className="list-disc list-inside space-y-0.5 text-slate-600">
                                {analysis.drivers.map((d, i) => <li key={i}>{d}</li>)}
                            </ul>
                        </div>
                        <div>
                            <h5 className="text-xs font-bold text-slate-500 uppercase mb-1">Hypotheses</h5>
                            <ul className="list-disc list-inside space-y-0.5 text-slate-600">
                                {analysis.hypotheses.map((h, i) => <li key={i}>{h}</li>)}
                            </ul>
                        </div>
                    </div>

                    {/* Actionable Next Steps */}
                    <div className="mt-auto bg-indigo-50 p-3 rounded-lg border border-indigo-100">
                        <h5 className="text-xs font-bold text-indigo-800 uppercase mb-2 flex items-center gap-1">
                            <ShieldAlert size={12} /> Recommended Actions
                        </h5>
                        <ul className="space-y-1">
                            {analysis.next_actions.map((action, i) => (
                                <li key={i} className="flex gap-2 text-indigo-900">
                                    <span className="font-bold select-none">→</span>
                                    <span>{action}</span>
                                </li>
                            ))}
                        </ul>
                    </div>
                </div>
            )}
        </div>
    );
};

const AIAnalystPanel = ({ reports }) => {
    if (!reports) return null;

    return (
        <div className="mb-8">
            <h3 className="text-lg font-semibold text-slate-800 mb-4 px-1">AI Staff Analysis</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 items-start">
                {reports.map((report, idx) => {
                    let Icon = BarChart3;
                    let color = "bg-blue-500";

                    if (report.role.includes("Risk")) { Icon = ShieldAlert; color = "bg-red-500"; }
                    if (report.role.includes("Audience")) { Icon = Users; color = "bg-purple-500"; }

                    return <AnalystCard key={idx} report={report} icon={Icon} color={color} />;
                })}
            </div>
        </div>
    );
};

export default AIAnalystPanel;
