from autogen import AssistantAgent
from memory_store import get_memory
import httpx

class MarketAgent(AssistantAgent):
    def __init__(self, name="market_agent", market_api_url="http://localhost:8080/live-market-event", **kwargs):
        super().__init__(name=name, **kwargs)
        self.market_api_url = market_api_url

    def generate_reply(self, messages):
        user_msg = messages[-1]["content"]
        user_id = self._extract_user_id(messages)

        try:
            response = httpx.get(self.market_api_url, timeout=5.0)
            if response.status_code == 200:
                market_events = response.json().get("events", [])
                if not market_events:
                    return {"output": "No market events found for today."}
                event_list = "\n".join([f"- {event}" for event in market_events])
                return {"output": f"📅 Today's market events:\n{event_list}"}
            else:
                return {"output": f"x Market service returned {response.status_code}: {response.text}"}
        except Exception as e:
            return {"output": f"⚠️ Error contacting Market service: {str(e)}"}

    def _extract_user_id(self, messages):
        return "default_user"
