from fastapi import FastAPI

from learnpathly_langchain.schemas import LearningPathRequest, LearningPathResponse
from learnpathly_langchain.service import generate_learning_path

app = FastAPI(title="learnpathlyLangChain API", version="0.1.0")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/v1/learning-path", response_model=LearningPathResponse)
def create_learning_path(payload: LearningPathRequest) -> LearningPathResponse:
    return generate_learning_path(payload.query)
