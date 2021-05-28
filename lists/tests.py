from django.test import TestCase
from lists.models import Item


class HomePageTest(TestCase):
    def test_homepage_returns_correct_html(self):
        self.assertTemplateUsed(self.client.get("/"), "home.html")

    def test_can_save_a_post_request(self):
        item_text = "A new list item"
        response = self.client.post("/", data={"item_text": item_text})

        self.assertEqual(1, Item.objects.count())
        self.assertEqual(item_text, Item.objects.first().text)
        self.assertIn(item_text, response.content.decode())
        self.assertTemplateUsed(response, "home.html")


class ItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        first_text = "The first (ever) list item"
        first_item = Item()
        first_item.text = first_text
        first_item.save()

        second_text = "Item the second"
        second_item = Item()
        second_item.text = second_text
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(2, len(saved_items))

        self.assertEqual(first_text, saved_items[0].text)
        self.assertEqual(second_text, saved_items[1].text)
