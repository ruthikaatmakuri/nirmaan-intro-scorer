from fastapi import FastAPI
from pydantic import BaseModel
from app.scorer import calculate_final_score

app = FastAPI(title="Nirmaan AI Intro Scorer API")


class InputData(BaseModel):
    transcript: str
    duration_seconds: float = 30.0  # default from sample audio


@app.post("/score")
def score_intro(data: InputData):
    result = calculate_final_score(
        data.transcript,
        data.duration_seconds
    )
    return result
