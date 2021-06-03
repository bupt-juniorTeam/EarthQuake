from django.test import TestCase
from django.urls import resolve
from window.views import home_page

class URLTest(TestCase):
    def test_homepage(self):
        found=resolve('/window/')
        print(found.url_name)
        self.assertEqual(found.func,home_page)