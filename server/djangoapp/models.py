from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class CarMake(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class CarModel(models.Model):
    TYPE_CHOICES = [
        ("Sedan", "Sedan"),
        ("SUV", "SUV"),
        ("WAGON", "Wagon"),
        ("Hatchback", "Hatchback"),
        ("Coupe", "Coupe"),
        ("Convertible", "Convertible"),
        ("Minivan", "Minivan"),
        ("Pickup", "Pickup"),
        ("Other", "Other"),
    ]

    make = models.ForeignKey(CarMake, on_delete=models.CASCADE, related_name="models")
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=30, choices=TYPE_CHOICES, default="Other")
    year = models.IntegerField(
        validators=[MinValueValidator(2015), MaxValueValidator(2023)]
    )

    class Meta:
        ordering = ["make__name", "name", "-year"]
        unique_together = ("make", "name", "year")

    def __str__(self):
        return f"{self.year} {self.make.name} {self.name}"
