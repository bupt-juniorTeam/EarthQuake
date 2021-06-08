from django.db import models


# Create your models here.
from django.utils import timezone


class Location(models.Model):
    longitude = models.DecimalField(decimal_places=2, max_digits=5, default=0.0)
    latitude = models.DecimalField(decimal_places=2, max_digits=5, default=0.0)


class Resource(models.Model):
    url = models.CharField(max_length=255)
    name = models.CharField(max_length=255)


class EarthQuake(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE, default=None)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, default=None)
    time = models.DateTimeField(auto_now_add=True)
    city = models.CharField(max_length=255)
    magnitude = models.CharField(max_length=255)
