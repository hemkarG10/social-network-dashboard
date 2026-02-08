import React, { useState, useEffect } from 'react';
import { Users, TrendingUp, Award, ChevronRight } from 'lucide-react';
import axios from 'axios';

// Simple API call here to avoid circular dep issues or just keep it simple
const API_BASE_URL = 'http://127.0.0.1:8000';

const LandingPage = ({ onSelectInfluencer }) => {
    const [topInfluencers, setTopInfluencers] = useState({});
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchTop = async () => {
            try {
                const res = await axios.get(`${API_BASE_URL}/mock/top_influencers`);
                setTopInfluencers(res.data);
            } catch (err) {
                console.error("Failed to fetch top influencers", err);
            } finally {
                setLoading(false);
            }
        };
        fetchTop();
    }, []);

    return (
        <div className="max-w-6xl mx-auto px-4 py-12">
            <div className="text-center mb-16">
                <h1 className="text-4xl font-extrabold text-slate-900 mb-4">
                    Find the Perfect Partner <span className="text-indigo-600">Instantly</span>
                </h1>
                <p className="text-lg text-slate-500 max-w-3xl mx-auto">
                    Instantly audit any influencer's credibility and performance. Our AI analyzes engagement quality, checks for fake followers, and predicts ROI for video campaigns, helping you make data-driven partnership decisions.
                </p>
            </div>

            <div className="mb-8 flex items-center gap-2">
                <TrendingUp className="text-indigo-600" size={24} />
                <h2 className="text-2xl font-bold text-slate-800">Top Monthly Picks</h2>
            </div>

            {loading ? (
                <div className="grid md:grid-cols-3 gap-6">
                    {[1, 2, 3].map(i => (
                        <div key={i} className="h-64 bg-slate-100 rounded-xl animate-pulse"></div>
                    ))}
                </div>
            ) : (
                <div className="space-y-12">
                    {Object.entries(topInfluencers).map(([category, influencers]) => (
                        <div key={category}>
                            <h3 className="text-xl font-bold text-slate-700 mb-6 pl-2 border-l-4 border-indigo-500">{category}</h3>
                            <div className="grid md:grid-cols-3 gap-6">
                                {influencers.map((inf, idx) => (
                                    <div
                                        key={inf.id}
                                        className="bg-white rounded-xl shadow-sm border border-slate-200 p-6 hover:shadow-md hover:border-indigo-300 transition-all group relative"
                                    >
                                        <div className="flex justify-between items-start mb-4">
                                            <div className="bg-indigo-50 text-indigo-700 font-bold px-3 py-1 rounded-full text-xs uppercase tracking-wide">
                                                #{idx + 1} {inf.niche}
                                            </div>
                                        </div>

                                        <div
                                            onClick={() => onSelectInfluencer(inf.id)}
                                            className="cursor-pointer"
                                        >
                                            <h3 className="text-xl font-bold text-slate-900 mb-1 group-hover:text-indigo-600 transition-colors">@{inf.handle}</h3>
                                            <p className="text-slate-500 text-sm mb-6 capitalize">{inf.platform} • {inf.niche}</p>

                                            <div className="grid grid-cols-2 gap-4 mb-6">
                                                <div>
                                                    <div className="text-slate-400 text-xs font-medium uppercase">Followers</div>
                                                    <div className="font-semibold text-slate-800">{(inf.followers / 1000000).toFixed(1)}M</div>
                                                </div>
                                                <div>
                                                    <div className="text-slate-400 text-xs font-medium uppercase">Est. Cost</div>
                                                    <div className="font-semibold text-slate-800">${inf.pricing.reel.toLocaleString()}</div>
                                                </div>
                                            </div>
                                        </div>

                                        <div className="flex items-center justify-between mt-4 pt-4 border-t border-slate-100">
                                            <div
                                                onClick={() => onSelectInfluencer(inf.id)}
                                                className="flex items-center text-indigo-600 text-sm font-semibold gap-1 hover:gap-2 transition-all cursor-pointer"
                                            >
                                                Audit Profile <ChevronRight size={16} />
                                            </div>
                                            <button className="text-xs font-medium text-slate-600 hover:text-indigo-600 px-3 py-1.5 rounded-full border border-slate-200 hover:border-indigo-200 transition-colors">
                                                Reach Out
                                            </button>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default LandingPage;
