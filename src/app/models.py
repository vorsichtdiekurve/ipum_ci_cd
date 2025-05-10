from pydantic import BaseModel


class PredictSentimentRequest(BaseModel):
    text: str


class PredictSentimentResponse(BaseModel):
    sentiment: list[str]
