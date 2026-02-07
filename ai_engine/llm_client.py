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

    def _mock_performance_analyst(self, data: Dict, rng: random.Random) -> List[Dict]:
        inf = data.get("influencer", {})
        camp = data.get("campaign", {})
        followers = inf.get("followers", 10000)
        engagement = inf.get("engagement_rate", 2.0)
        budget = camp.get("budget", 5000)
        
        # Simple deterministic logic
        impressions = int(followers * (0.2 + (rng.random() * 0.1))) # 20-30% reach
        engagements = int(impressions * (engagement / 100))
        conversions = int(impressions * (rng.uniform(0.005, 0.02))) # 0.5-2% conversion
        revenue = conversions * rng.uniform(50, 150) # $50-$150 AOV
        cpa = budget / max(1, conversions)
        min_roi = round(max(0.1, (revenue / budget) * 0.8), 2)
        max_roi = round(min_roi * 1.5, 2)

        return [
            {
                "kpi_id": "predicted_impressions",
                "value": impressions,
                "score_normalized": min(100, impressions / 10000),
                "explanation": f"Based on {followers:,} followers and historical reach patterns.",
                "confidence_score": 0.85
            },
            {
                "kpi_id": "predicted_engagements",
                "value": engagements,
                "score_normalized": min(100, engagements / 500),
                "explanation": f"Projected from {engagement}% engagement rate.",
                "confidence_score": 0.8
            },
            {
                "kpi_id": "predicted_conversions",
                "value": conversions,
                "score_normalized": min(100, conversions / 50),
                "explanation": "Estimated conversion rate of ~1% based on niche benchmarks.",
                "confidence_score": 0.7
            },
            {
                "kpi_id": "predicted_revenue",
                "value": f"${int(revenue):,}",
                "score_normalized": min(100, revenue / (budget * 2) * 50),
                "explanation": f"Assuming avg order value of $100.",
                "confidence_score": 0.65
            },
            {
                "kpi_id": "predicted_cpa",
                "value": f"${int(cpa)}",
                "score_normalized": max(0, 100 - (cpa / 10)),
                "explanation": "Cost per acquisition based on total spend.",
                "confidence_score": 0.75
            },
            {
                "kpi_id": "roi_confidence_range",
                "value": f"{min_roi}x - {max_roi}x",
                "score_normalized": min(100, min_roi * 30),
                "explanation": "Conservative to Optimistic ROI spread.",
                "confidence_score": 0.9
            }
        ]

    def _mock_risk_analyst(self, data: Dict, rng: random.Random) -> List[Dict]:
        return [
            {
                "kpi_id": "brand_safety_score",
                "value": rng.randint(60, 99),
                "score_normalized": rng.randint(60, 99), # same
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
                "score_normalized": 100 - rng.randint(5, 30), # Inverted for quality
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

    def _mock_audience_strategist(self, data: Dict, rng: random.Random) -> List[Dict]:
        return [
             {
                "kpi_id": "authenticity_score",
                "value": rng.randint(50, 95),
                "score_normalized": rng.randint(50, 95), 
                "explanation": "Comments appear organic and relevant.",
                "confidence_score": 0.9
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
