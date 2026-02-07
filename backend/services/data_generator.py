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

    def generate_influencer(self, influencer_id: str = None) -> Dict:
        """
        Generates a deterministic influencer profile based on the ID (or random if None).
        If ID is provided, the same ID will always produce the same data (seeded by ID).
        """
        if not influencer_id:
            influencer_id = str(uuid.UUID(int=self.rng.getrandbits(128)))
        
        # Seed the RNG with the influencer ID for determinism
        # Use stable hash of the ID
        seed_int = int(hashlib.md5(influencer_id.encode('utf-8')).hexdigest(), 16)
        local_seed = seed_int % 1000000 
        local_rng = random.Random(local_seed)

        niche = local_rng.choice(NICHES)
        platform = local_rng.choice(PLATFORMS)
        
        # Follower count logic (Skewed towards micro-influencers)
        # range: 10k to 5M
        followers = int(local_rng.expovariate(1/500000)) + 10000
        followers = min(followers, 10000000) # Cap at 10M

        # Realism Rule: Engagement rate inversely correlates with follower count
        # Base engagement: 1% to 8%
        # Decay factor based on log of followers
        base_engagement = local_rng.uniform(1.5, 8.0)
        decay_factor = 1.0 - (min(followers, 1000000) / 2000000) # Decay slightly with size
        engagement_rate = max(0.5, base_engagement * decay_factor)
        engagement_rate = round(engagement_rate, 2)

        # Hidden Truths (The "Real" params)
        bot_percentage = local_rng.uniform(5, 45) # 5% to 45% fake
        true_authenticity = max(0, 100 - bot_percentage - local_rng.randint(0, 20)) # Authenticity penalty for bots
        
        # Pricing Logic
        cpm = 10.0 # Base CPM
        if niche in ["Tech", "Finance"]: cpm *= 1.5
        if platform == "YouTube": cpm *= 2.0
        
        avg_likes = int(followers * (engagement_rate / 100))
        
        price_post = round((followers / 1000) * cpm, -1)
        
        return {
            "id": influencer_id,
            "handle": self._generate_handle(niche, local_rng),
            "platform": platform,
            "niche": niche,
            "followers": followers,
            "engagement_rate": engagement_rate,
            "avg_likes": avg_likes,
            "pricing": {
                "post": price_post,
                "story": price_post * 0.4,
                "reel": price_post * 1.2
            },
            "audience_demographics": {
                "female_pct": round(local_rng.uniform(10, 90), 1),
                "top_countries": ["US", "UK", "CA"]
            },
            "hidden_truth": {
                "true_authenticity_score": round(true_authenticity, 1),
                "true_engagement_quality": round(local_rng.uniform(40, 95), 1),
                "bot_percentage": round(bot_percentage, 1),
                "is_shadowbanned": local_rng.random() < 0.05
            }
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

    def get_top_influencers(self) -> List[Dict]:
        """Returns a curated list of top influencers for the landing page."""
        # Fixed list of IDs to ensure stability
        top_ids = ["tech-guru-99", "fashion-star-1", "fitness-pro-88", "gamer-x-22", "travel-bug-77"]
        profiles = []
        for pid in top_ids:
            # Generate profile but override some stats to make them "Top"
            profile = self.generate_influencer(pid)
            profile["followers"] = max(profile["followers"], 500000) # Ensure they are big
            profiles.append(profile)
        return profiles

# Global instance
generator = DataGenerator()
