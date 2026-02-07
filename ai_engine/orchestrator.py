from typing import Dict, Any, List
import os
from ai_engine.models import KPIOutput, AnalystResponse, ExecutiveResponse
from ai_engine.llm_client import llm_client

class Orchestrator:
    def __init__(self):
        self.prompts = self._load_prompts()

    def _load_prompts(self) -> Dict[str, str]:
        prompts = {}
        prompt_dir = os.path.join(os.path.dirname(__file__), "prompts")
        for filename in os.listdir(prompt_dir):
            if filename.endswith(".txt"):
                name = filename.replace(".txt", "")
                with open(os.path.join(prompt_dir, filename), "r") as f:
                    prompts[name] = f.read()
        return prompts

    def evaluate(self, influencer: Dict[str, Any], campaign: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main entry point. 
        1. Calls all 3 analysts (Performance, Risk, Audience).
        2. Aggregates results.
        3. Calls Executive Decider.
        4. Returns combined response.
        """
        context = {
            "influencer": influencer,
            "campaign": campaign
        }

        # 1. Analyst Phase (In a real system, these would be async/parallel)
        perf_data = llm_client.generate(self.prompts["performance_analyst"], context)
        risk_data = llm_client.generate(self.prompts["risk_analyst"], context)
        aud_data = llm_client.generate(self.prompts["audience_strategist"], context)

        # 2. Aggregation
        # Extract KPIs from the new structured response
        perf_kpis = perf_data.get("kpis", [])
        risk_kpis = risk_data.get("kpis", [])
        aud_kpis = aud_data.get("kpis", [])
        
        all_kpis = perf_kpis + risk_kpis + aud_kpis

        # 3. Executive Phase
        exec_context = {
            "analyst_reports": {
                "performance": perf_kpis,
                "risk": risk_kpis,
                "audience": aud_kpis
            },
            **context
        }
        
        decision = llm_client.generate(self.prompts["executive_decider"], exec_context)

        # 4. Final Package
        return {
            "decision_summary": decision,
            "kpis": all_kpis,
            "analyst_reports": [perf_data, risk_data, aud_data],
            "influencer_id": influencer.get("id"),
            "campaign_id": campaign.get("id"),
            "niche": influencer.get("niche", "General"),
            "goal": campaign.get("objective", "Awareness") # changed from 'goal' to 'objective' based on common Campaign schema
        }

# Global instance
orchestrator = Orchestrator()
