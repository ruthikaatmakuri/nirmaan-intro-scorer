import json
import re
from textblob import TextBlob
import language_tool_python

tool = language_tool_python.LanguageTool('en-US')

with open("app/rubric_config.json") as f:
    RUBRIC = json.load(f)


def count_words(text):
    return len(re.findall(r"\b\w+\b", text))


def check_keywords(text):
    results = {}
    lower = text.lower()

    for key in RUBRIC["content_checks"]:
        results[key] = True if key.replace("_", " ") in lower else False

    score = sum(results.values()) / len(results) * 40  # content weight applied later
    return score, results


def compute_speech_rate(word_count, duration_seconds):
    wpm = word_count / (duration_seconds / 60)

    for rule in RUBRIC["speech_rate_map"]:
        if rule["min"] <= wpm <= rule["max"]:
            return rule["score"], round(wpm, 2)

    return 2, wpm


def compute_grammar_score(text):
    matches = tool.check(text)
    errors = len(matches)

    for rule in RUBRIC["grammar_map"]:
        if rule["min"] <= errors <= rule["max"]:
            return rule["score"], errors

    return 2, errors


def compute_filler_score(text):
    words = text.lower().split()
    total = len(words)

    filler_count = sum(words.count(w) for w in RUBRIC["filler_words"])
    filler_rate = (filler_count / total) * 100

    for rule in RUBRIC["filler_rate_map"]:
        if rule["min"] <= filler_rate <= rule["max"]:
            return rule["score"], filler_rate

    return 3, filler_rate


def compute_sentiment(text):
    polarity = TextBlob(text).sentiment.polarity

    for rule in RUBRIC["sentiment_map"]:
        if rule["min"] <= polarity <= rule["max"]:
            return rule["score"], polarity

    return 3, polarity


def calculate_final_score(text, duration_seconds):
    words = count_words(text)

    content_score, content_details = check_keywords(text)
    speech_score, wpm = compute_speech_rate(words, duration_seconds)
    grammar_score, errors = compute_grammar_score(text)
    filler_score, filler_rate = compute_filler_score(text)
    sentiment_score, sentiment = compute_sentiment(text)

    final = (
        content_score * (RUBRIC["weights"]["content_structure"] / 40)
        + speech_score * (RUBRIC["weights"]["speech_rate"] / 10)
        + grammar_score * (RUBRIC["weights"]["language_grammar"] / 10)
        + filler_score * (RUBRIC["weights"]["clarity"] / 15)
        + sentiment_score * (RUBRIC["weights"]["engagement"] / 15)
    )

    return {
        "word_count": words,
        "wpm": wpm,
        "grammar_errors": errors,
        "filler_rate": filler_rate,
        "sentiment": sentiment,

        "section_scores": {
            "content_structure": content_score,
            "speech_rate": speech_score,
            "language_grammar": grammar_score,
            "clarity": filler_score,
            "engagement": sentiment_score
        },

        "content_details": content_details,
        "final_score": round(final, 2)
    }
