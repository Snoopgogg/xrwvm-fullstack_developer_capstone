import json
import logging
from pathlib import Path
import requests

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import CarModel
from .restapis import analyze_review_sentiments, get_request, post_review

logger = logging.getLogger(__name__)


def _json_body(request):
    try:
        return json.loads(request.body.decode("utf-8") or "{}")
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None


@csrf_exempt
def login_user(request):
    if request.method != "POST":
        return JsonResponse({"error": "Use POST"}, status=405)
    data = _json_body(request)
    if data is None:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    username = data.get("userName") or data.get("username")
    password = data.get("password")
    user = authenticate(request, username=username, password=password)
    if user is None:
        return JsonResponse({"userName": username or "", "status": "Invalid credentials"}, status=401)

    login(request, user)
    return JsonResponse({"userName": username, "status": "Authenticated"})


def logout_user(request):
    logout(request)
    return JsonResponse({"userName": "", "status": "Logged out"})


@csrf_exempt
def registration(request):
    if request.method != "POST":
        return JsonResponse({"error": "Use POST"}, status=405)
    data = _json_body(request)
    if data is None:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    username = (data.get("userName") or data.get("username") or "").strip()
    password = data.get("password") or ""
    first_name = (data.get("firstName") or data.get("first_name") or "").strip()
    last_name = (data.get("lastName") or data.get("last_name") or "").strip()
    email = (data.get("email") or "").strip()

    if not all([username, password, first_name, last_name, email]):
        return JsonResponse({"message": "All five fields are required"}, status=400)
    if User.objects.filter(username=username).exists():
        return JsonResponse({"message": "Username already exists"}, status=409)

    try:
        User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email,
        )
    except IntegrityError:
        return JsonResponse({"message": "Could not create this account"}, status=400)

    return JsonResponse({"status": 200, "message": "User successfully registered. You can now log in."})


def get_dealerships(request):
    try:
        dealers = get_request("fetchDealers")
        return JsonResponse({"status": 200, "dealers": dealers})
    except requests.RequestException as exc:
        logger.exception("Unable to retrieve dealerships")
        return JsonResponse({"status": 503, "error": str(exc), "dealers": []}, status=503)


def get_dealers_by_state(request, state):
    try:
        dealers = get_request(f"fetchDealers/{state}")
        return JsonResponse({"status": 200, "dealers": dealers})
    except Exception as exc:
        logger.exception("Unable to retrieve dealerships by state")
        return JsonResponse({"status": 503, "error": str(exc), "dealers": []}, status=503)


def get_dealer_details(request, dealer_id):
    try:
        dealers = get_request(f"fetchDealer/{dealer_id}")
        return JsonResponse({"status": 200, "dealer": dealers})
    except Exception as exc:
        logger.exception("Unable to retrieve dealer details")
        return JsonResponse({"status": 503, "error": str(exc), "dealer": []}, status=503)


def get_dealer_reviews(request, dealer_id):
    try:
        reviews = get_request(f"fetchReviews/dealer/{dealer_id}")
        for review in reviews:
            try:
                review["sentiment"] = analyze_review_sentiments(review.get("review", "")).get("sentiment", "neutral")
            except Exception:
                review["sentiment"] = "neutral"
        return JsonResponse({"status": 200, "reviews": reviews})
    except Exception as exc:
        logger.exception("Unable to retrieve dealer reviews")
        return JsonResponse({"status": 503, "error": str(exc), "reviews": []}, status=503)


@csrf_exempt
def add_review(request):
    if request.method != "POST":
        return JsonResponse({"error": "Use POST"}, status=405)
    data = _json_body(request)
    if data is None:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    required = ["name", "dealership", "review", "purchase", "purchase_date", "car_make", "car_model", "car_year"]
    missing = [key for key in required if key not in data]
    if missing:
        return JsonResponse({"status": 400, "error": "Missing fields: " + ", ".join(missing)}, status=400)
    try:
        saved = post_review(data)
        return JsonResponse({"status": 200, "message": "Review added successfully", "review": saved})
    except Exception as exc:
        logger.exception("Unable to save review")
        return JsonResponse({"status": 502, "error": str(exc)}, status=502)


def get_cars(request):
    cars = CarModel.objects.select_related("make").all()
    car_models = []
    seen_models = set()
    for car in cars:
        key = (car.make.name, car.name)
        if key not in seen_models:
            seen_models.add(key)
            car_models.append({"CarMake": car.make.name, "CarModel": car.name})

    if not car_models:
        data_file = (
            Path(__file__).resolve().parents[1]
            / "database" / "data" / "car_records.json"
        )
        with data_file.open(encoding="utf-8") as handle:
            records = json.load(handle).get("cars", [])
        seen = set()
        for car in records:
            key = (car["make"], car["model"])
            if key not in seen:
                seen.add(key)
                car_models.append({"CarMake": key[0], "CarModel": key[1]})
    return JsonResponse({"status": 200, "CarModels": car_models})


# Browser page views used by the capstone UI.
def home_page(request):
    return render(request, "Home.html", {"initial_state": ""})


def dealers_state_page(request, state):
    return render(request, "Home.html", {"initial_state": state})


def dealer_page(request, dealer_id):
    return render(request, "Dealer.html", {"dealer_id": dealer_id})


def post_review_page(request, dealer_id):
    return render(request, "PostReview.html", {"dealer_id": dealer_id})


def login_page(request):
    return render(request, "Login.html")


def register_page(request):
    return render(request, "Register.html")
