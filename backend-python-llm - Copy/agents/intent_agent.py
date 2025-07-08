from autogen import AssistantAgent
import os

intent_detection_agent = AssistantAgent(
    name="intent_detection_agent",
    system_message=(
        "You are an intent classifier. Classify the user's message into one of:\n"
        "predict_volume, get_market_events, explain_volume, default.\n"
        "Only return the label, no extra explanation."
    ),
    llm_config={
        "config_list": [
            {
                "model": "gpt-3.5-turbo",  # or gpt-4
                "api_key": os.getenv("OPENAI_API_KEY"),
            }
        ],
        "temperature": 0,
    }
)
