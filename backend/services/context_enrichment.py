from typing import Dict, Any

class ContextEnricher:
    """
    Enriches raw metric data with qualitative context, definitions, and business impact explanations.
    Acts as a "Consultant Layer" between the data and the user.
    """

    # Static Corpus of Definitions
    METRIC_DEFINITIONS = {
        "engagement_rate": {
            "definition": "Engagement rate measures active interaction (likes, comments, shares) relative to followers.",
            "base_importance": "High engagement signals that the audience is real and interested."
        },
        "avg_percentage_viewed": {
            "definition": "Completion rate / Avg % Viewed measures how well the content holds attention until the end.",
            "base_importance": "The ultimate 'truth' metric for content quality."
        },
        "stayed_vs_swiped": {
            "definition": "Stayed vs. Swiped measures the influencer's ability to stop the scroll.",
            "base_importance": "If users swipe away instantly, your brand message is never seen."
        },
        "predicted_saves": {
            "definition": "Saves indicate high intent and future purchase potential.",
            "base_importance": "A strong signal for utility and product interest."
        },
        "predicted_shares": {
            "definition": "Shares represent 'earned' reach and personal endorsement.",
            "base_importance": "Shows the content resonated enough to recommend to others."
        },
        "promo_code_redemptions": {
            "definition": "The most direct way to measure ROI and tie collaboration to revenue.",
            "base_importance": "Critical for bottom-line performance measurement."
        },
        "avg_view_duration": {
            "definition": "Average View Duration (AVD) checks if viewers stayed long enough to reach the hook.",
            "base_importance": "Vital for ensuring your product mention is actually seen."
        },
        "comment_sentiment_quality": {
            "definition": "Qualitative proof of engagement looking for product-specific questions.",
            "base_importance": "Distinguishes between fan-girling and actual buyer intent."
        },
        "brand_safety_score": {
            "definition": "Measures the risk of association with controversial topics.",
            "base_importance": "Protects brand reputation."
        },
        "fake_follower_probability": {
            "definition": "Bot percentage reveals the authenticity of the audience.",
            "base_importance": "High bots mean you are paying for ghost eyes."
        }
    }

    def enrich_metric(self, metric_key: str, value: Any, score_normalized: float, category: str, goal: str) -> Dict[str, Any]:
        """
        Main method to build the 'Consultant Card' JSON.
        """
        # 1. Base Definition
        def_data = self.METRIC_DEFINITIONS.get(metric_key, {
            "definition": "Key performance indicator.",
            "base_importance": "Important for overall performance."
        })

        # 2. Category Context
        importance_reason = self._get_category_context(metric_key, def_data["base_importance"], category)

        # 3. Score Verdict
        verdict = self._get_score_verdict(score_normalized)

        # 4. Business Impact
        business_implication = self._get_business_impact(metric_key, score_normalized, goal)

        return {
            "metric_name": metric_key.replace("_", " ").title(),
            "value": str(value),
            "context": {
                "definition": def_data["definition"],
                "importance_reason": importance_reason,
                "performance_verdict": verdict,
                "business_implication": business_implication
            }
        }

    def _get_category_context(self, metric: str, base_reason: str, category: str) -> str:
        """Injects category-specific nuance."""
        cat_lower = category.lower()
        
        if "saves" in metric:
            if "tech" in cat_lower:
                return "For Tech, saves are critical as users often bookmark tutorials and specs for later reference."
            if "fashion" in cat_lower:
                return "For Fashion, saves often act as a 'wishlist' for future shopping trips."
            if "food" in cat_lower:
                return "For Food, saves usually indicate users planning to cook this recipe."

        if "engagement" in metric:
            if "beauty" in cat_lower:
                return "For Beauty, high engagement is crucial as it signals trust in specific product recommendations."
            if "gaming" in cat_lower:
                return "For Gaming, community interaction is the primary driver of loyalty."

        return base_reason

    def _get_score_verdict(self, score: float) -> str:
        """NLTK Sentiment Simulation"""
        if score >= 85:
            return "Market-Leading (Excellent)"
        if score >= 70:
            return "Strong (Good)"
        if score >= 50:
            return "Average (Acceptable)"
        if score >= 40:
            return "Below Average (Concerning)"
        return "Critical Risk (Poor)"

    def _get_business_impact(self, metric: str, score: float, goal: str) -> str:
        """Connects back to the campaign goal (Awareness vs Conversion)"""
        is_good = score >= 50
        goal_lower = goal.lower()

        if "awareness" in goal_lower:
            if "view" in metric or "impression" in metric or "reach" in metric:
                 return "High views are perfect here, as your primary goal is Awareness." if is_good else "Low reach effectively fails the primary Awareness objective."
            if "engagement" in metric:
                 return "Engagement helps algorithmic reach, amplifying your Awareness goal." if is_good else "Low engagement might limit the viral spread needed for Awareness."

        if "conversion" in goal_lower:
             if "view" in metric:
                 return "High views are nice, but without interactions, they may not drive your Conversion goal."
             if "engagement" in metric or "save" in metric or "redemption" in metric:
                 return "This high intent directly supports your Conversion goal." if is_good else "The low intent signals here are a red flag for Conversion campaigns."

        # Default generic impact
        return "This directly impacts campaign efficiency."

# Global instance
context_enricher = ContextEnricher()
