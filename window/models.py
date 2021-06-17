from django.db import models

# Create your models here.
from django.utils import timezone


class Earthquake(models.Model):
    source = models.CharField(max_length=3)
    where = models.CharField(max_length=12)
    when = models.CharField(max_length=14)
    longitude = models.DecimalField(decimal_places=2, max_digits=5, default=0)
    latitude = models.DecimalField(decimal_places=2, max_digits=5, default=0)


class Set(models.Model):
    earthquake = models.ForeignKey(Earthquake, on_delete=models.CASCADE, default=None)
    set = models.CharField(max_length=3)
    count = models.IntegerField()


class Affection(models.Model):
    set = models.ForeignKey(Set, on_delete=models.CASCADE, default=None)
    index = models.CharField(max_length=3)
    grade = models.CharField(max_length=1)
