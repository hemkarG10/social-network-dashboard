from fastapi import APIRouter, HTTPException
from backend.services.data_generator import generator
import uuid

router = APIRouter(prefix="/mock", tags=["Mock Data"])

@router.get("/top_influencers")
def get_top_influencers():
    return generator.get_top_influencers()

@router.get("/influencer/{influencer_id}")
async def get_influencer(influencer_id: str):
    """
    Get a specific influencer by ID. 
    The data is deterministically generated from the ID.
    """
    try:
        # Validate UUID format just to be safe, though not strictly required by logic
        uuid_obj = uuid.UUID(influencer_id) 
    except ValueError:
        pass # We allow non-UUID strings too, generator handles it (by hashing or just using it)
        # Actually generator expects UUID string for exact reconstruction in my logic, 
        # let's just pass the string.

    data = generator.generate_influencer(influencer_id)
    return data

@router.get("/campaign")
async def get_random_campaign():
    """Get a random new campaign brief"""
    return generator.generate_campaign_brief()
