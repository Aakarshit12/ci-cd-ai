def analyze_text(text: str) -> dict:
    text_lower = text.lower()

    if any(word in text_lower for word in ["good", "great", "excellent", "happy"]):
        sentiment = "positive"
    elif any(word in text_lower for word in ["bad", "terrible", "sad", "angry"]):
        sentiment = "negative"
    else:
        sentiment = "neutral"

    return {
        "sentiment": sentiment,
        "confidence": 0.85
    }
