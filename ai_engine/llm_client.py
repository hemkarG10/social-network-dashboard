import json
import hashlib
import random
from typing import Dict, List, Any

class MockLLMClient:
    """
    Simulates an LLM for the MVP.
    Generates deterministic, schema-compliant JSON responses based on input hashes.
    This allows the system to work immediately without API keys or costs.
    """

    def generate(self, system_prompt: str, user_data: Dict[str, Any]) -> Any:
        # Create a stable seed from the input data
        # We assume user_data is JSON serializable
        data_str = json.dumps(user_data, sort_keys=True)
        seed_hash = hashlib.md5((system_prompt + data_str).encode('utf-8')).hexdigest()
        seed_int = int(seed_hash, 16)
        rng = random.Random(seed_int)

        # Detect which role we are simulating based on system prompt content
        if "You are the Performance Analyst" in system_prompt:
            return self._mock_performance_analyst(user_data, rng)
        elif "You are the Risk Analyst" in system_prompt:
            return self._mock_risk_analyst(user_data, rng)
        elif "You are the Audience Strategist" in system_prompt:
            return self._mock_audience_strategist(user_data, rng)
        elif "You are the Executive Decision Engine" in system_prompt:
            return self._mock_executive(user_data, rng)
        else:
            return {}

    def _generate_analysis_report(self, role: str, kpis: List[Dict], rng: random.Random) -> Dict:
        """
        Generates a structured TikTok-style PM analysis report.
        """
        # 1. Headline
        headlines = [
            "Performance is stabilizing vs baseline.",
            "Significant volatility detected in key metrics.",
            "Efficiency metrics are outperforming benchmarks.",
            "Engagement quality shows downward trend."
        ]
        headline = rng.choice(headlines)

        # 2. Magnitude (Delta)
        delta = rng.randint(-15, 25)
        sign = "+" if delta > 0 else ""
        magnitude = f"{sign}{delta}% vs 30d baseline"

        # 3. Drivers (Segments)
        segments = ["Gen Z (18-24)", "Tier 1 Cities", "Android Users", "New Followers", "Loyalists"]
        drivers = [
            f"Strong adoption in {rng.choice(segments)} segment.",
            f"Drop-off detected in {rng.choice(segments)} cohort.",
            f"High retention among {rng.choice(segments)}."
        ]
        
        # 4. Hypotheses
        hypotheses = [
            "Content format aligns well with current algorithm preference.",
            "Posting time caused initial reach suppression.",
            "Creative fatigue likely setting in for core audience.",
            "High shareability drove viral uplift."
        ]

        # 5. Next Actions
        actions = [
            "Verify lift with a Brand Lift Study.",
            "A/B test hook variations for retention.",
            "Deep dive into negative sentiment clusters.",
            "Scale budget in top-performing geo."
        ]

        return {
            "headline": headline,
            "magnitude": magnitude,
            "drivers": rng.sample(drivers, 2),
            "hypotheses": rng.sample(hypotheses, 2),
            "next_actions": rng.sample(actions, 2),
            "confidence_score": 0.85
        }

    def _mock_performance_analyst(self, data: Dict, rng: random.Random) -> Dict:
        inf = data.get("influencer", {})
        camp = data.get("campaign", {})
        followers = inf.get("followers", 10000)
        engagement = inf.get("engagement_rate", 2.0)
        budget = camp.get("budget", 5000)
        
        # Simple deterministic logic
        impressions = int(followers * (0.2 + (rng.random() * 0.1))) 
        engagements = int(impressions * (engagement / 100))
        conversions = int(impressions * (rng.uniform(0.005, 0.02)))
        revenue = conversions * rng.uniform(50, 150)
        cpa = budget / max(1, conversions)
        min_roi = round(max(0.1, (revenue / budget) * 0.8), 2)
        max_roi = round(min_roi * 1.5, 2)

        # New Business Metrics
        completion_rate = round(rng.uniform(0.15, 0.45), 2)
        saves = int(impressions * rng.uniform(0.02, 0.08))
        shares = int(impressions * rng.uniform(0.01, 0.05))
        avd = round(rng.uniform(3.5, 12.0), 1)
        stayed_rate = round(rng.uniform(0.6, 0.9), 2)
        promo_redemptions = int(conversions * rng.uniform(0.4, 0.8))

        kpis = [
            {
                "kpi_id": "predicted_impressions",
                "value": impressions,
                "score_normalized": min(100, impressions / 10000),
                "explanation": f"Based on {followers:,} followers and historical reach patterns.",
                "confidence_score": 0.85
            },
            {
                "kpi_id": "avg_percentage_viewed",
                "value": f"{int(completion_rate*100)}%",
                "score_normalized": int(completion_rate * 200),
                "explanation": "High retention indicates strong hook effectiveness.",
                "confidence_score": 0.8
            },
            {
                "kpi_id": "stayed_vs_swiped",
                "value": f"{int(stayed_rate*100)}% Stayed",
                "score_normalized": int(stayed_rate * 100),
                "explanation": "Measures ability to stop the scroll.",
                "confidence_score": 0.85
            },
            {
                "kpi_id": "avg_view_duration",
                "value": f"{avd}s",
                "score_normalized": min(100, int(avd * 8)),
                "explanation": "Average time spent watching content.",
                "confidence_score": 0.75
            },
            {
                "kpi_id": "predicted_saves",
                "value": saves,
                "score_normalized": min(100, saves / 100),
                "explanation": "High intent signal for product interest.",
                "confidence_score": 0.7
            },
            {
                "kpi_id": "predicted_shares",
                "value": shares,
                "score_normalized": min(100, shares / 100),
                "explanation": "Viral potential and earned reach.",
                "confidence_score": 0.65
            },
            {
                "kpi_id": "promo_code_redemptions",
                "value": promo_redemptions,
                "score_normalized": min(100, promo_redemptions / 20),
                "explanation": "Direct revenue attribution estimate.",
                "confidence_score": 0.6
            },
            {
                "kpi_id": "predicted_revenue",
                "value": f"${int(revenue):,}",
                "score_normalized": min(100, revenue / (budget * 2) * 50),
                "explanation": f"Assuming avg order value of $100.",
                "confidence_score": 0.65
            },
             {
                "kpi_id": "roi_confidence_range",
                "value": f"{min_roi}x - {max_roi}x",
                "score_normalized": min(100, min_roi * 30),
                "explanation": "Conservative to Optimistic ROI spread.",
                "confidence_score": 0.9
            }
        ]

        return {
            "role": "Performance Analyst",
            "kpis": kpis,
            "analysis": self._generate_analysis_report("Performance Analyst", kpis, rng)
        }

    def _mock_risk_analyst(self, data: Dict, rng: random.Random) -> Dict:
        kpis = [
            {
                "kpi_id": "brand_safety_score",
                "value": rng.randint(60, 99),
                "score_normalized": rng.randint(60, 99), 
                "explanation": "Content analysis shows mostly safe topics.",
                "confidence_score": 0.95
            },
            {
                "kpi_id": "controversy_probability",
                "value": f"{rng.randint(1, 20)}%",
                "score_normalized": rng.randint(1, 20),
                "explanation": "Low volatility in sentiment history.",
                "confidence_score": 0.8
            },
            {
                "kpi_id": "fake_follower_probability",
                "value": f"{rng.randint(5, 30)}%",
                "score_normalized": 100 - rng.randint(5, 30),
                "explanation": "Some engagement anomalies detected.",
                "confidence_score": 0.85
            },
             {
                "kpi_id": "platform_risk_score",
                "value": rng.choice(["Low", "Low", "Medium"]),
                "score_normalized": 80,
                "explanation": "Account is in good standing.",
                "confidence_score": 0.9
            }
        ]
        return {
            "role": "Risk Analyst",
            "kpis": kpis,
            "analysis": self._generate_analysis_report("Risk Analyst", kpis, rng)
        }

    def _mock_audience_strategist(self, data: Dict, rng: random.Random) -> Dict:
        kpis = [
             {
                "kpi_id": "authenticity_score",
                "value": rng.randint(50, 95),
                "score_normalized": rng.randint(50, 95), 
                "explanation": "Comments appear organic and relevant.",
                "confidence_score": 0.9
            },
            {
                "kpi_id": "comment_sentiment_quality",
                "value": f"{rng.randint(70, 95)}/100",
                "score_normalized": rng.randint(70, 95),
                "explanation": "High volume of product-specific questions vs generic emojis.",
                "confidence_score": 0.85
            },
            {
                "kpi_id": "engagement_quality",
                "value": rng.randint(40, 90),
                "score_normalized": rng.randint(40, 90),
                "explanation": "High ratio of replies vs likes.",
                "confidence_score": 0.85
            },
            {
                "kpi_id": "audience_brand_fit",
                "value": f"{rng.randint(30, 95)}%",
                "score_normalized": rng.randint(30, 95),
                "explanation": "Demographics align well with target.",
                "confidence_score": 0.85
            },
            {
                "kpi_id": "fatigue_index",
                "value": rng.randint(0, 60),
                "score_normalized": 100 - rng.randint(0, 60),
                "explanation": "Posting frequency is healthy.",
                "confidence_score": 0.9
            }
        ]
        return {
            "role": "Audience Strategist",
            "kpis": kpis,
            "analysis": self._generate_analysis_report("Audience Strategist", kpis, rng)
        }

    def chat(self, query: str, context: Dict) -> str:
        """
        Simulates a RAG chat response using the structured category-based context.
        Now uses ContextEnricher to return structured JSON explanations for specific metrics.
        Returns JSON strings for ALL responses to ensure UI consistency.
        """
        from backend.services.context_enrichment import context_enricher # Lazy import to avoid circular dependency if any
        import json

        query_lower = query.lower()
        
        # 0. Helper to find and enrich a specific metric
        def find_and_enrich_metric(keyword_list):
            # Flatten metrics from all categories to search
            all_metrics = []
            for cat in context.get("categories", {}).values():
                all_metrics.extend(cat.get("metrics", []))
            
            # Find matching metric
            for m in all_metrics:
                m_id = m['kpi_id']
                # fuzzy match
                if any(k in m_id for k in keyword_list):
                    enriched = context_enricher.enrich_metric(
                        metric_key=m_id,
                        value=m['value'],
                        score_normalized=m['score_normalized'] if 'score_normalized' in m else 75, # Fallback if score missing
                        category=context.get("niche", "General"),
                        goal=context.get("goal", "Awareness")
                    )
                    # Add type for frontend usage if needed, though frontend detects by 'metric_name' existence
                    enriched["type"] = "consultant_card" 
                    return json.dumps(enriched)
            return None

        # 0. Helper to format category analysis as JSON
        def format_category_card(category_name, title):
            cat = context.get("categories", {}).get(category_name)
            if not cat: return ""
            
            # Extract verdict from conclusion (simple heuristic or passed context)
            verdict = "Neutral"
            if "Strong" in cat['conclusion'] or "High" in cat['conclusion']: verdict = "Positive"
            if "Low" in cat['conclusion'] or "fail" in cat['conclusion'] or "Risk" in cat['conclusion']: verdict = "Concern"
            
            card = {
                "type": "analysis_card",
                "title": title,
                "verdict": verdict,
                "content": cat['conclusion'],
                "metrics": [{"label": m['kpi_id'].replace('_', ' ').title(), "value": str(m['value'])} for m in cat["metrics"]]
            }
            return json.dumps(card)

        # --- Metric Specific Queries ---

        # 1. Attention Metrics
        if any(w in query_lower for w in ["completion", "viewed"]):
            res = find_and_enrich_metric(["avg_percentage_viewed", "completion"])
            if res: return res
        if any(w in query_lower for w in ["stay", "swipe"]):
            res = find_and_enrich_metric(["stayed_vs_swiped"])
            if res: return res
        if "duration" in query_lower:
            res = find_and_enrich_metric(["avg_view_duration"])
            if res: return res

        # 2. Virality Metrics
        if "save" in query_lower:
             res = find_and_enrich_metric(["predicted_saves"])
             if res: return res
        if "share" in query_lower:
             res = find_and_enrich_metric(["predicted_shares"])
             if res: return res

        # 3. Conversion Metrics
        if any(w in query_lower for w in ["redemption", "code"]):
             res = find_and_enrich_metric(["promo_code_redemptions"])
             if res: return res
        if "cpa" in query_lower:
             res = find_and_enrich_metric(["predicted_cpa"])
             if res: return res

        # 4. Engagement / Audience Metrics
        if any(w in query_lower for w in ["engagement", "interact", "like", "comment"]):
             # "engagement_rate" might not exist, but "engagement_quality" does.
             res = find_and_enrich_metric(["engagement_quality", "engagement_rate", "comment_sentiment_quality"])
             if res: return res
             
        if "sentiment" in query_lower:
             res = find_and_enrich_metric(["comment_sentiment_quality", "sentiment"])
             if res: return res
             
        # 5. Risk / Safety Metrics
        if any(w in query_lower for w in ["safety", "scam", "fraud"]):
             res = find_and_enrich_metric(["brand_safety_score", "fake_follower", "bot"])
             if res: return res

        # --- Category / Broad Queries ---

        if any(w in query_lower for w in ["attention", "hook", "view", "watch"]):
            return format_category_card("Attention", "Attention Analysis")

        if any(w in query_lower for w in ["viral", "reach"]):
            return format_category_card("Virality", "Virality Assessment")
        
        if any(w in query_lower for w in ["roi", "money", "revenue", "convert", "sale"]):
            return format_category_card("Conversion", "Conversion Potential")

        if any(w in query_lower for w in ["risk", "bot"]):
            return format_category_card("Risk", "Risk Evaluation")

        if any(w in query_lower for w in ["audience", "fan", "demographic"]):
            return format_category_card("Audience", "Audience Analysis")

        # "Engagement" generic query should map to "Audience" category if no specific metric found above
        if "engagement" in query_lower:
             return format_category_card("Audience", "Engagement & Audience Analysis")

        # --- Smart Fallback ---
        
        # Safely extract executive data
        exec_data = context.get('executive_summary', {})
        if isinstance(exec_data, str):
            decision = "Review"
            risk_level = "UNKNOWN"
            # summary_text = exec_data # Unused currently
        else:
            decision = exec_data.get('decision', 'Review')
            risk_level = exec_data.get('risk_level', 'LOW') 
        
        fallback_content = (
            "I focus on performance, risk, and ROI analysis. "
            f"Based on the **{decision}** recommendation, "
            "here are the most relevant questions to ask:"
        )
        
        # Dynamic suggestions
        suggestions = []
        if risk_level == "HIGH" or "High" in str(exec_data):
            suggestions.append({"label": "Analyze Risk", "value": "Is it safe?"})
        
        suggestions.append({"label": "Check ROI", "value": "What is the ROI?"})
        suggestions.append({"label": "Audience Quality", "value": "How is the audience?"})

        fallback_card = {
            "type": "analysis_card",
            "title": "Out of Scope",
            "verdict": "Help", 
            "content": fallback_content,
            "metrics": suggestions
        }
        
        return json.dumps(fallback_card)

    def _mock_executive(self, data: Dict, rng: random.Random) -> Dict:
        # Simple synthesize logic
        risk_score = 0
        roi_potential = 0
        
        # In a real system, we'd parse the inputs.
        # Here we just re-roll consistent with the seed to simulate Synthesis
        
        decision = rng.choice(["GO", "GO", "TEST", "NO-GO"])
        risk = rng.choice(["LOW", "LOW", "MEDIUM", "HIGH"])
        
        # Enforce consistency rule: NO-GO if Risk is HIGH
        if risk == "HIGH":
            decision = "NO-GO"
            
        return {
            "decision": decision,
            "roi_prediction": {
                "min": round(rng.uniform(1.0, 2.5), 1),
                "max": round(rng.uniform(2.6, 5.0), 1),
                "confidence": 0.85
            },
            "risk_level": risk,
            "executive_summary": f"Based on the Strong ROI potential and {risk} risk profile, we recommend a {decision}.",
            "top_flags": [
                "ROI is projected to be positive.",
                f"Risk analysis indicates {risk} concern.",
                "Audience fit is within acceptable range."
            ]
        }

llm_client = MockLLMClient()
