import asyncio
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from agents.volume_agent import VolumeAgent
from agents.orchestrator_agent import OrchestratorAgent
from agents.market_agent import MarketAgent
from agents.explain_agent import ExplainAgent
from agents.default_agent import DefaultAgent
from agents.intent_agent import IntentAgent  # Your intent agent or llm agent for intent detection

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instantiate agents
volume_agent = VolumeAgent()
market_agent = MarketAgent()
explain_agent = ExplainAgent()
default_agent = DefaultAgent()
intent_agent = IntentAgent()  # Your LLM intent detection agent (class instance)

agents = {
    "predict_volume": volume_agent,
    "get_market_events": market_agent,
    "explain_volume": explain_agent,
    "default": default_agent,
}

orchestrator = OrchestratorAgent(user_proxy=None, agents=agents, llm_agent=intent_agent)

@app.post("/chat")
async def chat_endpoint(request: Request):
    data = await request.json()
    user_id = data.get("user_id", "default_user")
    message = data.get("message", "")

    response = await orchestrator.route(user_id, message)
    return {"response": response}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
