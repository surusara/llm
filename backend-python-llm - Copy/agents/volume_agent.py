from autogen import AssistantAgent
import httpx
from memory_store import get_memory

class VolumeAgent(AssistantAgent):
    def __init__(self, name="volume_agent", ml_api_url="http://localhost:8500/predict", **kwargs):
        super().__init__(name=name, **kwargs)
        self.ml_api_url = ml_api_url

    def generate_reply(self, messages):
        user_msg = messages[-1]["content"]
        user_id = self._extract_user_id(messages)

        context = get_memory(user_id)
        currency = context.get("currency")
        date = context.get("date")
        condition = context.get("market_condition")

        if not currency or not date:
            return {"output": "Currency or date missing. Please specify both."}

        payload = {
            "currency": currency,
            "date": date,
            "market_condition": condition or "Unknown"
        }

        try:
            response = httpx.post(self.ml_api_url, json=payload, timeout=5.0)
            if response.status_code == 200:
                result = response.json()
                volume = result.get("predicted_volume", "unknown")
                return {
                    "output": f"📊 Predicted volume for {currency} on {date} is **{volume} units** under condition: {condition or 'N/A'}."
                }
            else:
                return {"output": f"x ML service returned {response.status_code}: {response.text}"}
        except Exception as e:
            return {"output": f"⚠️ Error contacting ML service: {str(e)}"}

    def _extract_user_id(self, messages):
        return "default_user"
