from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import multiprocessing

# ML mock service
mock_ml = FastAPI()
# Java mock service
mock_java = FastAPI()

# Enable CORS
for app in [mock_ml, mock_java]:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

@mock_ml.post("/predict")
async def mock_predict(request: Request):
    data = await request.json()
    currency = data.get("currency", "Unknown")
    date = data.get("date", "Unknown")
    condition = data.get("market_condition", "Unknown")

    print(f"[MockML] Predicting for {currency} on {date} under {condition}")

    return {
        "volume": "1.2M",
        "currency": currency,
        "date": date,
        "market_condition": condition,
        "note": "This is a mock prediction response"
    }

@mock_java.get("/live-market-event")
async def mock_market_event():
    return {
        "description": "Mock: Scheduled ECB interest rate decision",
        "type": "Scheduled",
        "source": "Mock Java Service"
    }

# Function to run mock ML service
def run_mock_ml():
    uvicorn.run(mock_ml, host="0.0.0.0", port=8500)

# Function to run mock Java service
def run_mock_java():
    uvicorn.run(mock_java, host="0.0.0.0", port=8080)

if __name__ == "__main__":
    p1 = multiprocessing.Process(target=run_mock_ml)
    p2 = multiprocessing.Process(target=run_mock_java)

    p1.start()
    p2.start()

    p1.join()
    p2.join()
