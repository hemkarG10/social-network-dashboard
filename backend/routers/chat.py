from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.services.cache import cache
from ai_engine.llm_client import llm_client

router = APIRouter(prefix="/chat", tags=["Chat"])

class ChatRequest(BaseModel):
    query: str
    influencer_id: str

class ChatResponse(BaseModel):
    message: str

from backend.services.chat_context_builder import build_chat_context

@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    # 1. Retrieve Context from Cache
    # The cache stores the raw evaluation result (kpis, decision, etc.)
    evaluation_result = cache.get(request.influencer_id)
    
    if not evaluation_result:
        # If no context, we can't RAG.
        return ChatResponse(message="I don't have analysis data for this influencer yet. Please run an evaluation first.")

    # 2. Build Structured Context
    structured_context = build_chat_context(evaluation_result)

    # 3. Generate Response using Mock LLM (Simulated RAG)
    # We pass the formatted context now
    response = llm_client.chat(request.query, structured_context)
    
    return ChatResponse(message=response)
