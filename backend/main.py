from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import mock_data, evaluate, chat

app = FastAPI(title="AI Influencer Dashboard API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all for local dev ease
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(mock_data.router)
app.include_router(evaluate.router)
app.include_router(chat.router)

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "backend"}
