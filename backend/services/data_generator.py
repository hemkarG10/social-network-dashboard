import random
import uuid
import json
import hashlib
from typing import List, Dict

# Niches and Platforms
NICHES = ["Tech", "Beauty", "Fitness", "Gaming", "Fashion", "Food", "Travel"]
PLATFORMS = ["Instagram", "TikTok", "YouTube"]

class DataGenerator:
    def __init__(self, seed: int = 42):
        self.seed = seed
        self.rng = random.Random(seed)
        self.influencers_cache: Dict[str, Dict] = {}

    def _generate_handle(self, niche: str, rng: random.Random) -> str:
        prefixes = ["the", "real", "official", "daily", "just"]
        suffixes = ["life", "world", "vlogs", "reviews", "gram"]
        return f"{rng.choice(prefixes)}_{niche.lower()}_{rng.choice(suffixes)}_{rng.randint(1, 99)}"

    def generate_influencer(self, influencer_id: str = None, content_type: str = "all") -> Dict:
        """
        Generates a deterministic influencer profile based on the ID.
        Metric generation is influenced by content_type.
        """
        if not influencer_id:
            influencer_id = str(uuid.UUID(int=self.rng.getrandbits(128)))
        
        # Seed the RNG with the influencer ID for determinism
        seed_int = int(hashlib.md5(influencer_id.encode('utf-8')).hexdigest(), 16)
        local_seed = seed_int % 1000000 
        local_rng = random.Random(local_seed)

        niche = local_rng.choice(NICHES)
        platform = local_rng.choice(PLATFORMS)
        
        # Follower count logic
        followers = int(local_rng.expovariate(1/500000)) + 10000
        followers = min(followers, 10000000)

        # Base randomness factors
        quality_factor = local_rng.uniform(0.6, 1.0) # 0.6 = mediocre, 1.0 = star
        
        # --- 1. Engagement Quality ---
        # Adjust based on Content Type
        if content_type == "short":
            completion_rate = local_rng.uniform(0.4, 0.8) * quality_factor
            avg_view_duration_s = local_rng.uniform(15, 50) # Seconds
        elif content_type == "long":
            completion_rate = local_rng.uniform(0.2, 0.5) * quality_factor
            avg_view_duration_s = local_rng.uniform(120, 600)
        else: # all
            completion_rate = local_rng.uniform(0.3, 0.7) * quality_factor
            avg_view_duration_s = local_rng.uniform(30, 180)

        like_to_view = local_rng.uniform(0.05, 0.25) * quality_factor
        comment_to_view = like_to_view * 0.05
        share_ratio = like_to_view * 0.15
        
        # --- 2. Audience Credibility ---
        audience_quality_score = int(local_rng.uniform(40, 98) * quality_factor)
        subscriber_view_rate = local_rng.uniform(0.1, 0.4) * quality_factor
        follower_growth_rate = local_rng.uniform(-0.02, 0.15) * quality_factor # Monthly
        
        # --- 3. Intent & Conversion ---
        watch_to_subscribe = local_rng.uniform(0.01, 0.05) * quality_factor
        promo_redemption_rate = local_rng.uniform(0.001, 0.03) * quality_factor
        ctr_estimated = local_rng.uniform(0.005, 0.04) * quality_factor
        
        # --- 4. Consistency & Loyalty ---
        consistency_score = int(local_rng.uniform(50, 99))
        retention_score = int(completion_rate * 100)
        
        # --- 5. Brand Readiness ---
        brand_safety_score = int(local_rng.uniform(70, 100))
        overall_sentiment = int(local_rng.uniform(40, 95) * quality_factor)
        brand_collab_ratio = local_rng.uniform(0.01, 0.2) # 1% to 20% of posts are sponsored
        
        # --- 6. Growth Momentum ---
        predicted_growth_6m = followers * ((1 + follower_growth_rate)**6 - 1)
        predicted_views_next_3 = int(followers * subscriber_view_rate * 3)
        
        # --- 7. ROI & Forecasting ---
        cpm = 15.0 if niche in ["Tech", "Finance"] else 10.0
        est_cost = (followers / 1000) * cpm
        predicted_sales = (predicted_views_next_3 / 3) * ctr_estimated * 0.02 * 50 # Avg order value $50
        roi_ratio = predicted_sales / est_cost if est_cost > 0 else 0

        # Construct Detailed Metrics Dictionary
        detailed_metrics = {
            "engagement_quality": {
                "like_to_view_ratio": round(like_to_view * 100, 2),
                "comment_to_view_ratio": round(comment_to_view * 100, 2),
                "share_ratio": round(share_ratio * 100, 2),
                "completion_rate": round(completion_rate * 100, 1),
                "avg_view_duration": f"{int(avg_view_duration_s)}s",
                "comment_sentiment_quality": round(overall_sentiment * 0.9, 1) # Specific to comments
            },
            "audience_credibility": {
                "audience_quality_score": audience_quality_score,
                "subscriber_view_rate": round(subscriber_view_rate * 100, 1),
                "follower_growth_rate": round(follower_growth_rate * 100, 2)
            },
            "intent_conversion": {
                "watch_to_subscribe_ratio": round(watch_to_subscribe * 100, 2),
                "promo_redemption_rate": round(promo_redemption_rate * 100, 2),
                "ctr_estimated": round(ctr_estimated * 100, 2)
            },
            "consistency_loyalty": {
                "consistency_score": consistency_score,
                "retention_score": retention_score
            },
            "brand_readiness": {
                "brand_safety_score": brand_safety_score,
                "overall_sentiment_score": overall_sentiment,
                "brand_collaboration_ratio": round(brand_collab_ratio * 100, 1)
            },
            "growth_momentum": {
                "predicted_growth_6m": int(predicted_growth_6m),
                "predicted_views_next_3": predicted_views_next_3
            },
            "roi_forecasting": {
                "predicted_roi": round(roi_ratio, 1),
                "est_cost": int(est_cost)
            }
        }

        # Pricing for UI display (legacy structure support)
        price_post = round(est_cost, -1)
        
        return {
            "id": influencer_id,
            "handle": self._generate_handle(niche, local_rng),
            "platform": platform,
            "niche": niche,
            "followers": followers,
            "pricing": {
                "post": price_post,
                "reel": price_post * 1.2
            },
            "detailed_metrics": detailed_metrics,
            "content_type_context": content_type 
        }

    def generate_campaign_brief(self) -> Dict:
        """Generates a random campaign brief"""
        brand_categories = ["Fashion", "Tech", "Beauty", "Fitness"]
        category = self.rng.choice(brand_categories)
        budget = self.rng.choice([5000, 15000, 50000, 100000])
        
        return {
            "id": str(uuid.uuid4()),
            "brand_name": f"Nova{self.rng.choice(['Gear', 'Wear', 'Tech', 'Skin'])}",
            "category": category,
            "budget": budget,
            "goal": self.rng.choice(["Awareness", "Conversion"]),
            "platform_preference": [self.rng.choice(PLATFORMS)],
            "target_audience": {
                "age_range": "18-34",
                "interests": [category, "Lifestyle"]
            }
        }

    def get_top_influencers(self) -> Dict[str, List[Dict]]:
        """Returns a curated list of top influencers organized by category."""
        results = {}
        
        target_niches = ["Tech", "Beauty", "Fitness", "Gaming", "Travel"]
        
        for niche in target_niches:
            niche_influencers = []
            for i in range(1, 4):
                pid = f"top-{niche.lower()}-{i}"
                profile = self.generate_influencer(pid) # No content type needed for list
                
                profile["niche"] = niche 
                profile["followers"] = max(profile["followers"], 250000 * i)
                
                niche_influencers.append(profile)
            
            results[niche] = niche_influencers
            
        return results

# Global instance
generator = DataGenerator()
