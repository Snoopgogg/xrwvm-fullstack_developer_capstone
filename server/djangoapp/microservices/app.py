from flask import Flask, jsonify
from nltk.sentiment import SentimentIntensityAnalyzer

app = Flask("Sentiment Analyzer")

try:
    analyzer = SentimentIntensityAnalyzer()
except LookupError:
    # The bundled course image may not have the VADER lexicon installed.
    analyzer = None

POSITIVE_WORDS = {
    "amazing", "awesome", "best", "excellent", "fantastic", "good",
    "great", "happy", "helpful", "love", "perfect", "positive",
    "reliable", "wonderful"
}
NEGATIVE_WORDS = {
    "awful", "bad", "disappointing", "hate", "horrible", "poor",
    "negative", "terrible", "worst"
}


@app.get("/")
def home():
    return "Welcome to the Sentiment Analyzer. Use /analyze/text to get the sentiment"


@app.get("/analyze/<path:input_txt>")
def analyze_sentiment(input_txt):
    if analyzer is not None:
        scores = analyzer.polarity_scores(input_txt)
        positive = float(scores["pos"])
        negative = float(scores["neg"])
        neutral = float(scores["neu"])
        if negative > positive and negative > neutral:
            sentiment = "negative"
        elif neutral > positive and neutral > negative:
            sentiment = "neutral"
        else:
            sentiment = "positive"
    else:
        words = {word.strip(".,!?;:'\"").lower() for word in input_txt.split()}
        positive = len(words & POSITIVE_WORDS)
        negative = len(words & NEGATIVE_WORDS)
        sentiment = "positive" if positive > negative else (
            "negative" if negative > positive else "neutral"
        )

    return jsonify({"sentiment": sentiment})


if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5050")))
