import React, { useState, useEffect, useRef } from 'react';
import { Send, Bot, User, X } from 'lucide-react';
import { api } from '../services/api';

const ChatPanel = ({ influencerId, isOpen, onClose, isEmbedded = false }) => {
    const [messages, setMessages] = useState([
        { role: 'assistant', text: "Start chatting with me! I have analyzed this influencer's data. You can ask about Risk, ROI, or performance drivers." }
    ]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSend = async () => {
        if (!input.trim() || !influencerId) return;

        const userMsg = { role: 'user', text: input };
        setMessages(prev => [...prev, userMsg]);
        setInput('');
        setLoading(true);

        try {
            const response = await api.chatWithAI(influencerId, userMsg.text);
            const botMsg = { role: 'assistant', text: response.message };
            setMessages(prev => [...prev, botMsg]);
        } catch (err) {
            setMessages(prev => [...prev, { role: 'assistant', text: "Sorry, I encountered an error. Please try again." }]);
        } finally {
            setLoading(false);
        }
    };

    if (!isOpen && !isEmbedded) return null;

    // Conditional classes for Embedded vs Floating mode
    const containerClasses = isEmbedded
        ? "w-full h-full bg-white flex flex-col font-sans"
        : "fixed bottom-4 right-4 w-96 h-[500px] bg-white rounded-xl shadow-2xl border border-slate-200 flex flex-col z-50 overflow-hidden font-sans";

    const renderMessageContent = (text) => {
        try {
            const data = JSON.parse(text);

            // 1. Consultant Card (Metric Enrichment)
            if (data.metric_name && data.context) {
                return (
                    <div className="flex flex-col gap-3 min-w-[280px]">
                        {/* Header: Metric & Value */}
                        <div className="border-b border-indigo-100 pb-2 mb-1">
                            <h4 className="text-lg font-bold text-indigo-900">{data.metric_name}</h4>
                            <div className="text-2xl font-black text-indigo-600">{data.value}</div>
                        </div>

                        {/* Definition */}
                        <p className="text-xs text-slate-500 italic">
                            "{data.context.definition}"
                        </p>

                        {/* Category Context */}
                        <div className="text-sm text-slate-700 bg-indigo-50 p-2 rounded border border-indigo-100">
                            <strong>Why it matters:</strong> {data.context.importance_reason}
                        </div>

                        {/* Verdict Badge */}
                        <div className="flex items-center gap-2 mt-1">
                            <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Verdict:</span>
                            <span className={`px-2 py-1 rounded-full text-xs font-bold ${data.context.performance_verdict.includes("Excellent") || data.context.performance_verdict.includes("Strong")
                                    ? "bg-green-100 text-green-700"
                                    : data.context.performance_verdict.includes("Concern") || data.context.performance_verdict.includes("Risk")
                                        ? "bg-red-100 text-red-700"
                                        : "bg-yellow-100 text-yellow-800"
                                }`}>
                                {data.context.performance_verdict}
                            </span>
                        </div>

                        {/* Business Impact */}
                        <div className="mt-2 pl-3 border-l-4 border-indigo-500">
                            <h5 className="text-xs font-bold text-indigo-900 uppercase mb-1">Business Impact</h5>
                            <p className="text-sm text-slate-700 leading-snug">
                                {data.context.business_implication}
                            </p>
                        </div>
                    </div>
                );
            }

            // 2. Analysis Card (Category Summary)
            if (data.type === 'analysis_card') {
                return (
                    <div className="flex flex-col gap-2 min-w-[260px]">
                        <div className="flex justify-between items-center border-b border-indigo-100 pb-2">
                            <h4 className="font-bold text-indigo-800">{data.title}</h4>
                            <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full uppercase ${data.verdict === 'Positive' ? 'bg-green-100 text-green-700' :
                                    data.verdict === 'Concern' ? 'bg-red-100 text-red-700' : 'bg-slate-100 text-slate-600'
                                }`}>
                                {data.verdict}
                            </span>
                        </div>
                        <p className="text-sm text-slate-700">{data.content}</p>

                        {/* Metric Chips */}
                        <div className="flex flex-wrap gap-2 mt-1">
                            {data.metrics.map((m, i) => (
                                <div key={i} className="bg-slate-100 px-2 py-1 rounded text-xs text-slate-600 font-mono">
                                    {m.label}: <span className="font-bold text-slate-900">{m.value}</span>
                                </div>
                            ))}
                        </div>
                    </div>
                );
            }

            // 3. Simple Text (Wrapped in JSON)
            if (data.type === 'text') {
                return data.content;
            }

        } catch (e) {
            // Not JSON, render as plain text
        }
        return text;
    };

    return (
        <div className={containerClasses}>
            {/* Header - Only show close button if NOT embedded */}
            <div className="bg-indigo-600 p-4 text-white flex justify-between items-center shrink-0">
                <div className="flex items-center gap-2">
                    <Bot size={20} />
                    <h3 className="font-semibold">AI Assistant</h3>
                </div>
                {!isEmbedded && (
                    <button onClick={onClose} className="hover:bg-indigo-700 p-1 rounded">
                        <X size={18} />
                    </button>
                )}
            </div>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-slate-50">
                {messages.map((msg, idx) => (
                    <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                        <div className={`max-w-[85%] p-3 rounded-lg text-sm ${msg.role === 'user'
                            ? 'bg-indigo-600 text-white rounded-br-none'
                            : 'bg-white border border-slate-200 text-slate-700 rounded-bl-none shadow-sm'
                            }`}>
                            {renderMessageContent(msg.text)}
                        </div>
                    </div>
                ))}
                {loading && (
                    <div className="flex justify-start">
                        <div className="bg-white border border-slate-200 p-3 rounded-lg rounded-bl-none shadow-sm flex items-center gap-2">
                            <div className="w-2 h-2 bg-indigo-400 rounded-full animate-bounce"></div>
                            <div className="w-2 h-2 bg-indigo-400 rounded-full animate-bounce delay-100"></div>
                            <div className="w-2 h-2 bg-indigo-400 rounded-full animate-bounce delay-200"></div>
                        </div>
                    </div>
                )}
                <div ref={messagesEndRef} />
            </div>

            {/* Input */}
            <div className="p-3 bg-white border-t border-slate-200 flex gap-2 shrink-0">
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={(e) => e.key === 'Enter' && handleSend()}
                    placeholder="Ask about risk, ROI..."
                    className="flex-1 px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:border-indigo-500"
                    disabled={loading}
                />
                <button
                    onClick={handleSend}
                    disabled={loading || !input.trim()}
                    className="bg-indigo-600 text-white p-2 rounded-lg hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                    <Send size={18} />
                </button>
            </div>
        </div>
    );
};

export default ChatPanel;
