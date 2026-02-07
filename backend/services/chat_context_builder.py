from typing import Dict, List, Any

def build_chat_context(evaluation_result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Transforms the flat evaluation result into a structured, category-based context
    for the LLM Chat RAG system.
    """
    kpis = evaluation_result.get("kpis", [])
    
    # helper to find kpi value
    def get_kpi(kpi_id):
        return next((k for k in kpis if k["kpi_id"] == kpi_id), None)

    # 1. Attention Category
    attention_metrics = [
        get_kpi("avg_percentage_viewed"),
        get_kpi("stayed_vs_swiped"),
        get_kpi("avg_view_duration")
    ]
    attention_metrics = [m for m in attention_metrics if m] # filter None

    attention_conclusion = "Audience attention is inconsistent."
    # Simple logic for conclusion
    avg_viewed = get_kpi("avg_percentage_viewed")
    if avg_viewed:
        val = int(avg_viewed["value"].strip('%'))
        if val > 40:
            attention_conclusion = "Strong depth of viewing indicates high content resonance."
        elif val < 20:
            attention_conclusion = "Content is failing to hold attention past the hook."

    # 2. Virality Category
    virality_metrics = [
        get_kpi("predicted_shares"),
        get_kpi("predicted_saves")
    ]
    virality_metrics = [m for m in virality_metrics if m]

    virality_conclusion = "Low viral potential detected."
    shares = get_kpi("predicted_shares")
    if shares and isinstance(shares["value"], int) and shares["value"] > 500: # Arbitrary threshold for "high" in this mock
        virality_conclusion = "High shareability suggests potential for organic reach multiplier."

    # 3. Conversion Category
    conversion_metrics = [
        get_kpi("promo_code_redemptions"),
        get_kpi("predicted_cpa"),
        get_kpi("roi_confidence_range")
    ]
    conversion_metrics = [m for m in conversion_metrics if m]

    conversion_conclusion = "ROI is uncertain."
    roi = get_kpi("roi_confidence_range")
    if roi:
         # "2.5x - 3.5x" -> check lower bound
         try:
             lower_bound = float(roi["value"].split('x')[0])
             if lower_bound > 2.0:
                 conversion_conclusion = "Projected ROI is healthy and positive."
             else:
                 conversion_conclusion = "ROI margins are tight; optimization needed."
         except:
             pass

    # 4. Risk Category
    risk_metrics = [
        get_kpi("brand_safety_score"),
        get_kpi("controversy_probability"),
        get_kpi("fake_follower_probability")
    ]
    risk_metrics = [m for m in risk_metrics if m]
    
    risk_conclusion = "Risk profile is acceptable."
    safety = get_kpi("brand_safety_score")
    if safety and isinstance(safety["value"], int) and safety["value"] < 70:
        risk_conclusion = "CAUTION: Brand safety score is below recommended threshold."

    # 5. Audience / Engagement Category
    audience_metrics = [
        get_kpi("engagement_rate"),
        get_kpi("comment_sentiment_quality"),
        get_kpi("audience_brand_fit")
    ]
    audience_metrics = [m for m in audience_metrics if m]

    audience_conclusion = "Audience engagement is stable."
    er = get_kpi("engagement_rate")
    if er:
        # Check if high/low. Mock logic: > 3% is good?
        # Value is float? check mock generator. It returns float 2.0 etc.
        # But wait, mock generator returns it inside "influencer" dict, 
        # but orchestator puts "predicted_impressions" etc in kpis list.
        # DOES engagement_rate exist in kpis? 
        # Looking at Orchestrator... 
        # The Performance Analyst mock returns "predicted_impressions", "avg_percentage_viewed" etc.
        # It does NOT return "engagement_rate" as a KPI! it uses it to calculate others.
        # BUT "Audience Strategist" DOES return "engagement_quality" and "comment_sentiment_quality".
        # Let's use "engagement_quality" instead of "engagement_rate" if rate is missing.
        # actually Audience Strategist returns: authenticity_score, comment_sentiment_quality, engagement_quality, audience_brand_fit, fatigue_index.
        pass

    # Re-fetching correct metrics for Audience
    audience_metrics = [
        get_kpi("engagement_quality"),
        get_kpi("comment_sentiment_quality"),
        get_kpi("authenticity_score"),
         get_kpi("audience_brand_fit")
    ]
    audience_metrics = [m for m in audience_metrics if m]
    
    audience_conclusion = "Audience quality is solid."
    eq = get_kpi("engagement_quality")
    if eq and isinstance(eq["value"], int) and eq["value"] > 70:
        audience_conclusion = "High engagement quality suggests deep community trust."

    # Construct the final context
    structured_context = {
        "influencer_id": evaluation_result.get("influencer_id"),
        "niche": evaluation_result.get("niche", "General"),
        "goal": evaluation_result.get("goal", "Awareness"),
        "categories": {
            "Attention": {
                "metrics": attention_metrics,
                "conclusion": attention_conclusion
            },
            "Virality": {
                "metrics": virality_metrics,
                "conclusion": virality_conclusion
            },
            "Conversion": {
                "metrics": conversion_metrics,
                "conclusion": conversion_conclusion
            },
            "Risk": {
                "metrics": risk_metrics,
                "conclusion": risk_conclusion
            },
            "Audience": {
                "metrics": audience_metrics,
                "conclusion": audience_conclusion
            }
        },
        "executive_summary": evaluation_result.get("decision_summary", "No summary available.")
    }

    return structured_context
