from autogen import AssistantAgent

class ExplainAgent(AssistantAgent):
    def __init__(self, name="explain_agent", **kwargs):
        super().__init__(name=name, **kwargs)

    def generate_reply(self, messages):
        user_msg = messages[-1]["content"]
        # Simple canned explanation, or you could integrate with LLM here for richer replies
        explanation = (
            "This FX volume forecasting assistant uses historical data and market events "
            "to predict FX trade volumes. You can ask me to predict volumes, explain scenarios, "
            "or provide current market events."
        )
        return {"output": explanation}
