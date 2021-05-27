from django.test import TestCase


class HomePageTest(TestCase):
    def test_homepage_returns_correct_html(self):
        self.assertTemplateUsed(self.client.get("/"), "home.html")

    def test_can_save_a_post_request(self):
        response = self.client.post("/", data={"item_text": "A new list item"})
        self.assertIn("A new list item", response.content.decode())
        self.assertTemplateUsed(response, "home.html")
