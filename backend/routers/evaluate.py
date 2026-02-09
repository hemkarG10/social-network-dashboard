from fastapi import APIRouter, HTTPException
from ai_engine.orchestrator import orchestrator
from ai_engine.models import EvaluationRequest
from backend.services.data_generator import generator
from backend.services.cache import cache

router = APIRouter(prefix="/evaluate", tags=["Evaluation"])

@router.post("/")
async def evaluate_influencer(request: EvaluationRequest):
    """
    Evaluates an influencer against a campaign.
    Uses the AI Engine Orchestrator to compute KPIs and a decision.
    """
    # If the request contains only IDs (which we don't fully support in schema yet but might),
    # we would fetch them. For now, we assume full objects or fetch if IDs are passed.
    # To support the Frontend efficiently, let's allow passing IDs or full objects.
    # The current schema expects full objects in the dict.
    
    # Simple pass-through to orchestrator
    result = orchestrator.evaluate(request.influencer, request.campaign)
    return result

@router.post("/demo")
async def evaluate_demo(influencer_id: str, campaign_id: str = None, content_type: str = "all"):
    """
    Helper endpoint for the frontend.
    Fetches the mock data by ID, then runs evaluation.
    This saves the frontend from having to send massive JSON blobs.
    """
    # Check cache first (Cache key now includes content_type)
    cache_key = f"{influencer_id}_{content_type}"
    cached_result = cache.get(cache_key)
    if cached_result:
        return cached_result

    # Pass content_type to generator to influence metrics
    influencer = generator.generate_influencer(influencer_id, content_type)
    
    if campaign_id:
        # TODO: Implement get_campaign by ID if we add persistence. 
        # For now, generate a random one or use the one provided.
         campaign = generator.generate_campaign_brief() # Placeholder
    else:
        campaign = generator.generate_campaign_brief()
        
    result = orchestrator.evaluate(influencer, campaign)
    
    # Store in cache
    cache.set(cache_key, result)
    
    return result
