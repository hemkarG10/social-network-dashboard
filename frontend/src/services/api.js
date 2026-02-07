import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000';

export const api = {
    /**
     * Evaluates an influencer by ID. 
     * Uses the demo endpoint to let the backend generate the mock data.
     */
    evaluateDemo: async (influencerId, campaignId = null) => {
        try {
            const response = await axios.post(`${API_BASE_URL}/evaluate/demo`, null, {
                params: {
                    influencer_id: influencerId,
                    campaign_id: campaignId
                }
            });
            return response.data;
        } catch (error) {
            console.error("API Error:", error);
            throw error;
        }
    }
};
