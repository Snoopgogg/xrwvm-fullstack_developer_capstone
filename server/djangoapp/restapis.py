import os
from urllib.parse import quote

import requests
from dotenv import load_dotenv

load_dotenv()

backend_url = os.getenv("backend_url", "http://localhost:3030").rstrip("/")
sentiment_analyzer_url = os.getenv(
    "sentiment_analyzer_url", "http://localhost:5050"
).rstrip("/")


def get_request(endpoint, **kwargs):
    """GET JSON from the Node.js dealership service."""
    url = f"{backend_url}/{endpoint.lstrip('/')}"
    response = requests.get(url, params=kwargs or None, timeout=15)
    response.raise_for_status()
    return response.json()


def post_review(data_dict):
    """Submit a review to the Node.js dealership service."""
    url = f"{backend_url}/insert_review"
    response = requests.post(url, json=data_dict, timeout=15)
    response.raise_for_status()
    return response.json()


def analyze_review_sentiments(text):
    """Return the sentiment result for a review string."""
    url = f"{sentiment_analyzer_url}/analyze/{quote(str(text), safe='')}"
    response = requests.get(url, timeout=15)
    response.raise_for_status()
    return response.json()
