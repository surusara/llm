# backend-python-llm/agents/default_agent.py

from autogen import AssistantAgent

class DefaultAgent(AssistantAgent):
    def __init__(self, name="default_agent", **kwargs):
        system_message = (
            "You are a friendly and gentle chatbot assistant for FX analysts. "
            "Keep the tone light and soft. If users ask unrelated or vague questions, answer politely. "
            "You can also share fun facts or stats about the FX model like: "
            "'I've seen 20,000+ trade data points!'"
        )
        super().__init__(name=name, system_message=system_message, **kwargs)

    def generate_reply(self, messages):
        user_msg = messages[-1]["content"]

        if any(greet in user_msg.lower() for greet in ["hi", "hello", "hey"]):
            return {"output": "👋 Hello! How can I assist with FX volume today?"}

        return {"output": "I'm here to help with FX volume, market events, or just chat. What would you like to do?"}
