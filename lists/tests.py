from django.test import TestCase
from django.urls import resolve
from lists.views import home_page


class HomePageTest(TestCase):
    def test_homepage_returns_correct_html(self):
        self.assertTemplateUsed(self.client.get("/"), "home.html")
