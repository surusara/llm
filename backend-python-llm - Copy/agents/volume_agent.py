# agents/volume_agent.py

import httpx
from memory_store import get_memory

class VolumeAgent:
    def __init__(self, ml_api_url="http://localhost:8500/predict"):
        self.ml_api_url = ml_api_url

    async def generate_reply(self, user_input, user_id):
        context = get_memory(user_id)
        currency = context.get("currency")
        date = context.get("date")
        condition = context.get("market_condition")

        if not currency or not date:
            return "Currency or date missing. Please specify both."

        payload = {
            "currency": currency,
            "date": date,
            "market_condition": condition or "Unknown"
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(self.ml_api_url, json=payload, timeout=5.0)
                response.raise_for_status()
                result = response.json()
                volume = result.get("predicted_volume", "unknown")
                return f"📊 Predicted volume for {currency} on {date} is **{volume} units** under condition: {condition or 'N/A'}."
            except Exception as e:
                return f"⚠️ Error contacting ML service: {str(e)}"
