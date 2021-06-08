from django.test import TestCase
from django.urls import resolve
from .models import *
from window.views import home_page


class URLTest(TestCase):
    def test_homepage(self):
        found = resolve('/window/')
        print(found.url_name)
        self.assertEqual(found.func, home_page)


class ModelTest(TestCase):
    def test_create_model(self):
        location = Location.objects.create(longitude=22.35, latitude=123.11)
        resource = Resource.objects.create(url="test", name="correct")
        earthquake = EarthQuake.objects.create(
            location=location, resource=resource, time=timezone.now(), city="233331100000", magnitude="特大"
        )
        self.assertEqual(EarthQuake.objects.count(), 1)
