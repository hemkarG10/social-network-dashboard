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
        # Extract Detailed Metrics from Data Generator
        detailed = data.get("detailed_metrics", {})
        growth_metrics = detailed.get("growth_momentum", {})
        intent_metrics = detailed.get("intent_conversion", {})
        c_type = data.get("content_type", "all")
        
        # --- Restore Logic for Granular Metrics ---
        inf = data.get("influencer", {})
        camp = data.get("campaign", {})
        followers = inf.get("followers", 10000)
        engagement = inf.get("engagement_rate", 2.0)
        budget = camp.get("budget", 5000)

        # Simple deterministic logic for execution metrics
        impressions = int(followers * (0.2 + (rng.random() * 0.1))) 
        completion_rate = round(rng.uniform(0.15, 0.45), 2)
        saves = int(impressions * rng.uniform(0.02, 0.08))
        stayed_rate = round(rng.uniform(0.6, 0.9), 2)
        conversions = int(impressions * (rng.uniform(0.005, 0.02)))
        promo_redemptions = int(conversions * rng.uniform(0.4, 0.8))

        # 1. Growth Momentum
        # Base value on predicted growth
        growth_val = int(growth_metrics.get("predicted_growth_6m", 0) / 1000) # Simple scaling
        growth_score = min(99, int(rng.uniform(60, 95))) # Mock score for now, or derive from growth rate
        
        growth_explanation = "Viral peaks indicate strong short-term momentum."
        if c_type == "long":
            growth_explanation = "Consistent channel growth suggests long-term stability."

        # 2. Intent Strength
        intent_score = min(99, int(intent_metrics.get("promo_redemption_rate", 0) * 2000)) # Scale up
        intent_score = max(40, intent_score)
        
        intent_explanation = "High share ratio indicates content stops the scroll."
        if c_type == "long":
            intent_explanation = "High retention correlates with strong conversion intent."

        kpis = [
            # --- Strategic Signals (Top 5) ---
            {
                "kpi_id": "growth_momentum",
                "value": f"{growth_score}/100",
                "score_normalized": growth_score,
                "explanation": growth_explanation,
                "confidence_score": 0.85
            },
            {
                "kpi_id": "intent_strength",
                "value": f"{intent_score}/100",
                "score_normalized": intent_score,
                "explanation": intent_explanation,
                "confidence_score": 0.82
            },
            
            # --- Granular Execution Metrics (Restored) ---
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
                "kpi_id": "predicted_saves",
                "value": saves,
                "score_normalized": min(100, saves / 100),
                "explanation": "High intent signal for product interest.",
                "confidence_score": 0.7
            },
            {
                "kpi_id": "promo_code_redemptions",
                "value": promo_redemptions,
                "score_normalized": min(100, promo_redemptions / 20),
                "explanation": "Direct revenue attribution estimate.",
                "confidence_score": 0.6
            }
        ]

        return {
            "role": "Performance Analyst",
            "kpis": kpis,
            "analysis": self._generate_analysis_report("Performance Analyst", kpis, rng)
        }

    def _mock_risk_analyst(self, data: Dict, rng: random.Random) -> Dict:
        detailed = data.get("detailed_metrics", {})
        brand_metrics = detailed.get("brand_readiness", {})
        c_type = data.get("content_type", "all")

        safety_score = brand_metrics.get("brand_safety_score", 85)
        
        # Contextual explanation
        explanation = "Content aligns with brand safety guidelines."
        if c_type == "short":
            explanation = "Low viral risk detected in recent shorts."
        elif c_type == "long":
            explanation = "Deep content reflects strong brand alignment."

        kpis = [
            # --- Strategic Signals (Top 5) ---
            {
                "kpi_id": "brand_readiness",
                "value": f"{safety_score}/100",
                "score_normalized": safety_score,
                "explanation": explanation,
                "confidence_score": 0.95
            },
            
            # --- Granular Execution Metrics (Restored) ---
            {
                "kpi_id": "brand_safety_score",
                "value": safety_score, # Re-using the raw score
                "score_normalized": safety_score, 
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
            }
        ]
        return {
            "role": "Risk Analyst",
            "kpis": kpis,
            "analysis": self._generate_analysis_report("Risk Analyst", kpis, rng)
        }

    def _mock_audience_strategist(self, data: Dict, rng: random.Random) -> Dict:
        detailed = data.get("detailed_metrics", {})
        eng_metrics = detailed.get("engagement_quality", {})
        cred_metrics = detailed.get("audience_credibility", {})
        loyalty_metrics = detailed.get("consistency_loyalty", {})
        c_type = data.get("content_type", "all")

        # 1. Engagement Quality
        # Composite of completion and like/view
        comp = eng_metrics.get("completion_rate", 50) 
        # comp is 0-100 from DataGenerator? No, it's 0.3-0.8 * 100 in dict?
        # In generator: round(completion_rate * 100, 1) -> so it's 0-100.
        eng_score = int(comp)
        
        eng_explanation = "High completion rates indicate strong hook."
        if c_type == "long":
            eng_explanation = "Deep engagement duration suggests high interest."

        kpis = [
             # --- Strategic Signals (Top 5) ---
             {
                "kpi_id": "engagement_quality",
                "value": f"{eng_score}/100",
                "score_normalized": eng_score, 
                "explanation": eng_explanation,
                "confidence_score": 0.9
            }
        ]

        # 2. Audience Signal (Credibility vs Loyalty)
        if c_type == "long":
            # Audience Loyalty
            retention = loyalty_metrics.get("retention_score", 70)
            kpis.append({
                "kpi_id": "audience_loyalty",
                "value": f"{retention}/100",
                "score_normalized": retention,
                "explanation": "Consistent viewership across long-form content.",
                "confidence_score": 0.88
            })
        else:
            # Audience Credibility (Short or All)
            qual = cred_metrics.get("audience_quality_score", 80)
            kpis.append({
                "kpi_id": "audience_credibility",
                "value": f"{qual}/100",
                "score_normalized": qual,
                "explanation": "Audience appears authentic with low bot probability.",
                "confidence_score": 0.88
            })
            
        # --- Granular Execution Metrics (Restored) ---
        kpis.extend([
            {
                "kpi_id": "comment_sentiment_quality",
                "value": f"{detailed.get('engagement_quality', {}).get('comment_sentiment_quality', 85)}/100",
                "score_normalized": 85,
                "explanation": "High volume of product-specific questions vs generic emojis.",
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
                "kpi_id": "avg_view_duration", # Moved from performance sometimes?? No, keep logical separation. 
                # Actually, let's just restore what was there.
                "kpi_id": "fatigue_index",
                "value": rng.randint(0, 60),
                "score_normalized": 100 - rng.randint(0, 60),
                "explanation": "Posting frequency is healthy.",
                "confidence_score": 0.9
            }
        ])

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

import os
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

class RealLLMClient:
    """
    Real integration with OpenAI GPT-4o-mini (or similar).
    Uses the same interface as MockLLMClient.
    """
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o-mini" # Cost effective and fast

    def generate(self, system_prompt: str, user_data: Dict[str, Any]) -> Any:
        try:
            # Prepare the user message with the data context
            user_content = f"Here is the data context:\n{json.dumps(user_data, indent=2)}"
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content}
                ],
                response_format={"type": "json_object"},
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            return json.loads(content)
        except Exception as e:
            print(f"LLM Error: {e}")
            # Fallback to mock on error? Or just raise? 
            # For reliability in this hybrid setup, getting SOMETHING is better.
            print("Falling back to Mock Client due to error.")
            return MockLLMClient().generate(system_prompt, user_data)

# ... (MockLLMClient remains as is, but we will instantiate based on env)

# Selector Logic
api_key = os.environ.get("OPENAI_API_KEY")

if api_key and OPENAI_AVAILABLE:
    print("🚀 Using Real LLM Client (OpenAI)")
    llm_client = RealLLMClient(api_key)
else:
    print("🤖 Using Mock LLM Client (Deterministic)")
    if api_key and not OPENAI_AVAILABLE:
        print("   (OpenAI Key found but 'openai' package not installed. Run `pip install openai`)")
    llm_client = MockLLMClient()
