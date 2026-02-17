from app.core.ai import analyze_text


def test_analyze_text_positive():
    result = analyze_text("This is a great day")
    assert result["sentiment"] == "positive"


def test_analyze_text_negative():
    result = analyze_text("This is a terrible day")
    assert result["sentiment"] == "negative"


def test_analyze_text_neutral():
    result = analyze_text("Just an ordinary statement")
    assert result["sentiment"] == "neutral"

