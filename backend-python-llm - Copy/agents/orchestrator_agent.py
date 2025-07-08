# agents/orchestrator_agent.py

from memory_store import update_memory, get_memory

class OrchestratorAgent:
    def __init__(self, intent_agent, agents):
        """
        :param intent_agent: instance of IntentDetectionAgentAPI
        :param agents: dict of other agents, each with async `generate_reply(user_input, user_id)` method
        """
        self.intent_agent = intent_agent
        self.agents = agents

    async def detect_intent(self, user_input):
        intent = await self.intent_agent.detect_intent(user_input)
        print(f"[Orchestrator] Intent detected: {intent}")
        return intent

    def extract_entities(self, user_input):
        # You can implement your normalize_currency and parse_date here or import them
        from utils import normalize_currency, parse_date
        currency = normalize_currency(user_input)
        date = parse_date(user_input)
        return {"currency": currency, "date": date}

    async def route(self, user_id, user_input):
        intent = await self.detect_intent(user_input)

        # Update memory with entities
        entities = self.extract_entities(user_input)
        for k, v in entities.items():
            if v:
                update_memory(user_id, k, v)

        # Special handling if needed
        if intent == "predict_volume":
            market_condition = await self.agents["market_agent"].generate_reply(user_input, user_id)
            update_memory(user_id, "market_condition", market_condition)

        target_agent = self.agents.get(intent) or self.agents["default"]
        reply = await target_agent.generate_reply(user_input, user_id)

        return reply or "No response"
