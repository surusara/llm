# agents/intent_agent.py

import os
import httpx
import asyncio

class IntentDetectionAgentAPI:
    def __init__(self, api_url=None, api_key=None):
        self.api_url = api_url or os.getenv("LLM_INTENT_API_URL", "http://localhost:9000/intent")
        self.api_key = api_key or os.getenv("LLM_API_KEY")

    async def detect_intent(self, user_input: str) -> str:
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are an intent classifier. Classify the user's message into one of:\n"
                        "predict_volume, get_market_events, explain_volume, default.\n"
                        "Only return the label, no extra explanation."
                    ),
                },
                {
                    "role": "user",
                    "content": user_input,
                },
            ],
            "temperature": 0
        }

        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(self.api_url, json=payload, headers=headers, timeout=10.0)
                response.raise_for_status()
                data = response.json()
                intent = data["choices"][0]["message"]["content"].strip().lower()
                valid_intents = {"predict_volume", "get_market_events", "explain_volume", "default"}
                if intent not in valid_intents:
                    return "default"
                return intent
            except Exception as e:
                print(f"Error calling intent detection API: {e}")
                return "default"
