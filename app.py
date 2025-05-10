from fastapi import FastAPI
from src.inference import Inference
from settings import settings
from src.app.models import PredictSentimentResponse, PredictSentimentRequest

app = FastAPI()
inference = Inference(settings=settings)


@app.get("/health")
async def health():
    return 200


@app.get("/")
async def home():
    return {"INFO": "Go to '/docs' endpoint"}


@app.post("/predict")
async def predict(request: PredictSentimentRequest):
    return PredictSentimentResponse(sentiment=inference.predict(request.text))
