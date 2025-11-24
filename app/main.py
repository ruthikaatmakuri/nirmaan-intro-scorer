from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.scorer import calculate_final_score

app = FastAPI(title="Nirmaan AI Intro Scorer API")

# --- CORS so that your local frontend or GitHub Pages can call Render API ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # you can restrict later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class InputData(BaseModel):
    transcript: str
    duration_seconds: float = 30.0


@app.get("/")
def read_root():
    return {
        "message": "Nirmaan Intro Scorer API is running.",
        "usage": "Use POST /score or visit /docs for the interactive UI."
    }


@app.post("/score")
def score_intro(data: InputData):
    result = calculate_final_score(
        data.transcript,
        data.duration_seconds
    )
    return result
