from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any

class EvaluationRequest(BaseModel):
    influencer: Dict[str, Any]
    campaign: Dict[str, Any]

class KPIOutput(BaseModel):
    kpi_id: str
    value: Any
    score_normalized: float
    explanation: str
    confidence_score: float

class AnalysisReport(BaseModel):
    headline: str
    magnitude: str
    drivers: List[str]
    hypotheses: List[str]
    next_actions: List[str]
    confidence_score: float

class AnalystResponse(BaseModel):
    role: str
    kpis: List[KPIOutput]
    analysis: AnalysisReport

class ExecutiveResponse(BaseModel):
    decision: str
    roi_prediction: Dict[str, float]
    risk_level: str
    executive_summary: str
    top_flags: List[str]
