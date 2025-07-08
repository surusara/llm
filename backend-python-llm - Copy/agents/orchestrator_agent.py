from memory_store import update_memory, get_memory
from utils import normalize_currency, parse_date

class OrchestratorAgent:
    def __init__(self, user_proxy, agents, llm_agent):
        self.user_proxy = user_proxy
        self.agents = agents
        self.llm_agent = llm_agent

    async def detect_intent(self, user_input):
        prompt = (
            "You are an intent classification model for an FX volume assistant.\n"
            "Classify the user's intent into one of: predict_volume, get_market_events, explain_volume, default.\n"
            "Return ONLY the intent name.\n\n"
            f"User Input: \"{user_input}\"\n"
            "Intent:"
        )
        messages = [{"role": "user", "content": prompt}]
        
        response = await self.llm_agent.a_generate_reply(messages=messages)
        intent = response.strip().lower()
        valid_intents = {"predict_volume", "get_market_events", "explain_volume", "default"}
        if intent not in valid_intents:
            intent = "default"
        return intent

    def extract_entities(self, user_input):
        currency = normalize_currency(user_input)
        date = parse_date(user_input)
        return {"currency": currency, "date": date}

    async def route(self, user_id, user_input):
        intent = await self.detect_intent(user_input)
        print(f"[Orchestrator] Intent detected: {intent}")

        entities = self.extract_entities(user_input)
        for key, value in entities.items():
            if value:
                update_memory(user_id, key, value)

        if intent == "predict_volume":
            market_response = await self.agents["market_agent"].a_generate_reply(
                messages=[{"role": "user", "content": user_input}]
            )
            update_memory(user_id, "market_condition", market_response.get("output", ""))

        target_agent = self.agents.get(intent) or self.agents["default"]
        reply = await target_agent.a_generate_reply(messages=[{"role": "user", "content": user_input}])

        return reply.get("output", "No response")
