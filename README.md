📘 Nirmaan AI – Self Introduction Scorer

AI-powered tool that evaluates a student's spoken introduction using rule-based scoring, NLP-based scoring, and rubric-driven weights.

🚀 Overview

This project implements an AI tool that analyzes a student’s self-introduction transcript and produces:

Final Score (0–100)

Per-criterion scores

Grammar error count

Speech rate (WPM)

Clarity (filler-word rate)

Engagement (sentiment score)

Detailed content checklist

Word-level analysis

The tool follows the official Nirmaan AI Internship Case Study rubric, including:

Content & Structure (40%)

Speech Rate (10%)

Language & Grammar (20%)

Clarity (15%)

Engagement (15%)

🧠 Features

✔ Accept transcript text
✔ Rule-based content scoring (salutation, name, hobbies, family, etc.)
✔ Grammar checking (LanguageTool)
✔ Sentiment analysis (TextBlob polarity)
✔ Filler-word analysis
✔ Speech-rate scoring using rubric thresholds
✔ JSON API (FastAPI backend)
✔ Simple frontend UI (HTML + JS)
✔ Fully deployable on Render

📂 Project Structure
nirmaan-intro-scorer/
 ├─ app/
 │   ├─ main.py              # FastAPI backend
 │   ├─ scorer.py            # All scoring logic
 │   ├─ utils.py
 │   ├─ rubric_config.json   # Cleaned rubric extracted from Excel
 │   └─ __init__.py
 ├─ frontend/
 │   ├─ index.html           # Web UI for scoring
 ├─ requirements.txt         # Dependencies
 ├─ README.md                # Documentation
 └─ deployment_guide.md      # Render deployment steps

🛠 Tech Stack
Backend

FastAPI

Python 3

LanguageTool (Grammar checking)

TextBlob (Sentiment)

Regex & custom rule functions

Uvicorn server

Frontend

HTML

JavaScript (Fetch API)

Simple UI for scoring

Deployment

Render Web Service (Free Tier)

⚙️ API Endpoint
POST /score
Request Body:
{
  "transcript": "string",
  "duration_seconds": 30
}

Example Response:
{
  "word_count": 131,
  "wpm": 125.4,
  "grammar_errors": 3,
  "filler_rate": 1.52,
  "sentiment": 0.42,
  "section_scores": {
    "content_structure": 34,
    "speech_rate": 10,
    "language_grammar": 8,
    "clarity": 15,
    "engagement": 12
  },
  "content_details": {
    "salutation": true,
    "name": true,
    "hobby": true,
    "fun_fact": true,
    ...
  },
  "final_score": 86.4
}

▶️ How to Run Locally
1. Install dependencies
pip install -r requirements.txt

2. Initialize TextBlob (first time only)
from textblob import download_corpora
download_corpora()

3. Start backend server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

4. Open browser

Visit:

http://127.0.0.1:8000/docs

5. Run Frontend

Open:

frontend/index.html



📊 Rubric Logic Summary
1. Content & Structure (40%)

Based on checklist:

salutation

name

age

school

class

family details

hobbies

fun fact

unknown fact

favourite subject

motivation

ending statement

structure order

vocabulary richness (TTR)

2. Speech Rate (10%)

From your Excel:

WPM Range	Score
110–130	10
90–110	8
70–90	6
50–70	4
<50	2
3. Grammar (20%)

Based on grammar error count from LanguageTool:

Errors	Score
0–2	10
3–5	8
6–8	6
9–12	4
>12	2
4. Clarity (15%)

Filler word rate:

Filler %	Score
<2%	15
2–4%	12
4–6%	9
6–10%	6
>10%	3
5. Engagement (15%)

Sentiment score:

Polarity	Score
>0.6	15
0.4–0.6	12
0.2–0.4	9
0–0.2	6
<0	3
🎥 Demo Video Requirement

As per case study instructions:

You must include:

Running backend locally

Scoring a transcript

Frontend UI usage

Render deployment demo

Showing final output

🙌 Author

ATMAKURI RUTHIKA
Nirmaan AI Internship Case Study Project# nirmaan-intro-scorer
