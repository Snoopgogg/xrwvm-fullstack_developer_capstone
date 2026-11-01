import json
from pathlib import Path

from django.db import transaction

from .models import CarMake, CarModel


def initiate():
    """Load the supplied car inventory into the Django catalogue."""
    data_file = (
        Path(__file__).resolve().parents[1]
        / "database"
        / "data"
        / "car_records.json"
    )

    if not data_file.exists():
        raise FileNotFoundError(f"Car catalogue not found: {data_file}")

    with data_file.open(encoding="utf-8") as handle:
        records = json.load(handle).get("cars", [])

    with transaction.atomic():
        for record in records:
            make_name = record["make"].strip()
            model_name = record["model"].strip()
            year = int(record["year"])
            car_type = record.get("bodyType", "Other")
            if year < 2015 or year > 2023:
                continue

            make, _ = CarMake.objects.get_or_create(
                name=make_name,
                defaults={"description": f"{make_name} vehicle manufacturer"},
            )
            CarModel.objects.get_or_create(
                make=make,
                name=model_name,
                year=year,
                defaults={"type": car_type if car_type else "Other"},
            )

    return {
        "makes": CarMake.objects.count(),
        "models": CarModel.objects.count(),
    }
