# AI Influencer Dashboard (MVP)

A comprehensive AI-powered platform for brands to audit, analyze, and evaluate influencers. This tool replaces gut feelings with data-driven insights, utilizing a multi-agent AI system to assess Performance, Risk, and Audience Fit.

## 🚀 Key Features

### 1. **AI-Powered Audit**
   - **Executive Summary**: Get an immediate "Go", "No Go", or "Review" decision.
   - **Multi-Agent Analysis**:
     - **Performance Analyst**: Evaluates reach, engagement, and consistency.
     - **Risk Analyst**: Scans for brand safety issues, controversy, and fake followers.
     - **Audience Strategist**: Determines fit for specific campaign goals (e.g., Awareness vs. Conversion).

### 2. **Interactive AI Consultant**
   - **Context-Aware Chat**: Ask specific questions about the influencer's data (e.g., "Why is the risk high?").
   - **Deep Dive Cards**: The AI responds with structured "Analysis Cards" and "Consultant Cards" rather than just text.
   - **Smart Fallback**: Gracefully handles out-of-scope queries with helpful suggestions.

### 3. **Visual Dashboard**
   - **KPI Cards**: Instant view of Engagement Rate, View Duration, and Sentiment.
   - **Confidence Scores**: Transparency on how confident the AI is in its assessment.
   - **Dynamic UI**: React-based interface with TailwindCSS for a premium feel.

---

## 🛠 Tech Stack

- **Frontend**: React (Vite), TailwindCSS, Lucide Icons
- **Backend**: FastAPI (Python)
- **AI Engine**: 
  - **Mock LLM Client**: A deterministic simulation of an LLM for cost-free, reliable testing. 
  - **RAG-Lite Architecture**: Retrieval-Augmented Generation logic to inject audit results into the chat context.

---

## 🏁 Getting Started

### Prerequisites
- **Python 3.9+**
- **Node.js 16+** & **npm**

### Installation

1.  **Clone the repository**
    ```bash
    git clone <repository_url>
    cd ai-influencer-dashboard
    ```

2.  **Backend Setup**
    ```bash
    # Navigate to the root (where backend/ is)
    # Create a virtual environment (optional but recommended)
    python3 -m venv venv
    source venv/bin/activate

    # Install dependencies
    pip install fastapi uvicorn pydantic openai
    ```

    **Optional: Enable Real AI**
    To use real GPT-4 analysis instead of mock data:
    ```bash
    export OPENAI_API_KEY="sk-..."
    ```
    *If no key is provided, the system defaults to the Mock LLM automatically.*

3.  **Frontend Setup**
    ```bash
    cd frontend
    npm install
    ```

### Running the Application

You need to run the backend and frontend in separate terminals.

**Terminal 1: Backend**
```bash
# From the project root
python3 -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```
*The API will be available at `http://127.0.0.1:8000`. API Docs at `http://127.0.0.1:8000/docs`.*

**Terminal 2: Frontend**
```bash
# From the frontend/ directory
npm run dev
```
*The UI will be available at `http://localhost:5173`.*

---

## 📂 Project Structure

```
├── ai_engine/           # Core AI Logic
│   ├── llm_client.py    # Mock LLM and Prompt Engineering
│   ├── orchestrator.py  # Coordinates the 3 Analysts + Executive
│   └── models.py        # Pydantic models for AI responses
├── backend/             # FastAPI Server
│   ├── routers/         # API Endpoints (evaluate, chat, mock_data)
│   └── services/        # Business Logic (Context Builder, Enrichment)
├── frontend/            # React Application
│   ├── src/components/  # UI Components (KPI Cards, Chat Panel)
│   └── src/App.jsx      # Main Dashboard Layout
├── shared-schemas/      # JSON Schemas shared between services
└── README.md            # You are here
```

## 🧪 Usage Guide

1.  **Open the Dashboard** at `http://localhost:5173`.
2.  **Evaluate an Influencer**: Use one of the mock handles:
    - `fitness-pro-88` (High Performance, Low Risk)
    - `fashion-diva-01` (High Viral, Moderate Risk)
    - `tech-guru-99` (Good engagement, Niche appeal)
    - `travel-bug-77` (Mixed performance)
3.  **View the Report**: Analyze the "Executive Summary" and detailed metrics.
4.  **Ask the Assistant**: Click the "Assistant & Deep Dive" tab.
    - Try asking: *"What is the ROI?"*, *"Is this influencer safe?"*.
    - Try an unknown query: *"What is the capital of France?"* to see the Smart Fallback.

---

**Note**: This is an MVP implementation using a Mock LLM for demonstration purposes. In a production environment, `ai_engine/llm_client.py` would be replaced with an adapter for OpenAI GPT-4 or Anthropic Claude.
