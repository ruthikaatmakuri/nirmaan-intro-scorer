import json
import re
from textblob import TextBlob

# Load rubric config
with open("app/rubric_config.json") as f:
    RUBRIC = json.load(f)


def count_words(text: str) -> int:
    return len(re.findall(r"\b\w+\b", text))


def check_keywords(text: str):
    """
    Very simple content checklist based on presence of key phrases.
    """
    results = {}
    lower = text.lower()

    for key in RUBRIC["content_checks"]:
        # convert "special_thing_about_family" -> "special thing about family"
        phrase = key.replace("_", " ")
        results[key] = phrase in lower

    # raw content score out of 40 (max weight for this section)
    coverage = sum(results.values()) / len(results) if results else 0
    score = coverage * 40
    return score, results


def compute_speech_rate(word_count: int, duration_seconds: float):
    if duration_seconds <= 0:
        duration_seconds = 1
    wpm = word_count / (duration_seconds / 60.0)

    for rule in RUBRIC["speech_rate_map"]:
        if rule["min"] <= wpm <= rule["max"]:
            return rule["score"], round(wpm, 2)

    # fallback lowest score
    return 2, round(wpm, 2)


def compute_grammar_score(text: str):
    """
    Approximate grammar issues using TextBlob:
    - Compute TextBlob's corrected text
    - Count how many words differ -> treat as 'errors'
    This is a heuristic substitute for language_tool_python (no Java).
    """
    original_words = re.findall(r"\b\w+\b", text)
    corrected_text = str(TextBlob(text).correct())
    corrected_words = re.findall(r"\b\w+\b", corrected_text)

    # align lengths
    n = min(len(original_words), len(corrected_words))
    errors = 0
    for i in range(n):
        if original_words[i].lower() != corrected_words[i].lower():
            errors += 1

    # map error count to score using rubric
    for rule in RUBRIC["grammar_map"]:
        if rule["min"] <= errors <= rule["max"]:
            return rule["score"], errors

    return 2, errors


def compute_filler_score(text: str):
    words = text.lower().split()
    total = len(words) if words else 1

    filler_list = RUBRIC["filler_words"]
    filler_count = 0
    for fw in filler_list:
        filler_count += words.count(fw)

    filler_rate = (filler_count / total) * 100.0

    for rule in RUBRIC["filler_rate_map"]:
        if rule["min"] <= filler_rate <= rule["max"]:
            return rule["score"], round(filler_rate, 2)

    return 3, round(filler_rate, 2)


def compute_sentiment(text: str):
    polarity = TextBlob(text).sentiment.polarity

    for rule in RUBRIC["sentiment_map"]:
        if rule["min"] <= polarity <= rule["max"]:
            return rule["score"], round(polarity, 3)

    return 3, round(polarity, 3)


def calculate_final_score(text: str, duration_seconds: float):
    words = count_words(text)

    # section scores
    content_score, content_details = check_keywords(text)
    speech_score, wpm = compute_speech_rate(words, duration_seconds)
    grammar_score, errors = compute_grammar_score(text)
    filler_score, filler_rate = compute_filler_score(text)
    sentiment_score, sentiment = compute_sentiment(text)

    # combine with rubric weights
    w = RUBRIC["weights"]
    final = (
        content_score * (w["content_structure"] / 40.0)
        + speech_score * (w["speech_rate"] / 10.0)
        + grammar_score * (w["language_grammar"] / 10.0)
        + filler_score * (w["clarity"] / 15.0)
        + sentiment_score * (w["engagement"] / 15.0)
    )

    return {
        "word_count": words,
        "wpm": wpm,
        "grammar_errors_estimated": errors,
        "filler_rate_percent": filler_rate,
        "sentiment_polarity": sentiment,
        "section_scores": {
            "content_structure": round(content_score, 2),
            "speech_rate": speech_score,
            "language_grammar": grammar_score,
            "clarity": filler_score,
            "engagement": sentiment_score,
        },
        "content_details": content_details,
        "final_score": round(final, 2),
    }
