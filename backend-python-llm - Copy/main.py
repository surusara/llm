import asyncio
from fastapi import FastAPI, Request
from agents.intent_agent import IntentDetectionAgentAPI
from agents.orchestrator_agent import OrchestratorAgent
from agents.volume_agent import VolumeAgent

# import MarketAgent, ExplainAgent similarly

app = FastAPI()

# Instantiate your agents
intent_agent = IntentDetectionAgentAPI()

volume_agent = VolumeAgent()
# Instantiate market_agent and explain_agent accordingly
market_agent = ...  # your MarketAgent instance
explain_agent = ...  # your ExplainAgent instance

agents = {
    "predict_volume": volume_agent,
    "get_market_events": market_agent,
    "explain_volume": explain_agent,
    "default": explain_agent,
}

orchestrator = OrchestratorAgent(intent_agent=intent_agent, agents=agents)


@app.post("/chat")
async def chat_endpoint(request: Request):
    data = await request.json()
    user_id = data.get("user_id", "default_user")
    message = data.get("message", "")

    response = await orchestrator.route(user_id, message)
    return {"response": response}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8501)
