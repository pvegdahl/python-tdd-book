from django.test import TestCase
from lists.models import Item


class HomePageTest(TestCase):
    def test_homepage_returns_correct_html(self):
        self.assertTemplateUsed(self.client.get("/"), "home.html")

    def test_can_save_a_post_request(self):
        item_text = "A new list item"
        self.client.post("/", data={"item_text": item_text})
        self.assertEqual(1, Item.objects.count())
        self.assertEqual(item_text, Item.objects.first().text)

    def test_redirects_after_post(self):
        response = self.client.post("/", data={"item_text": "The item text"})
        self.assertEqual(302, response.status_code)
        self.assertEqual("/lists/the-only-list-in-the-world", response["location"])

    def test_only_save_items_when_necessary(self):
        self.client.get("/")
        self.assertEqual(0, Item.objects.count())

    def test_display_all_list_items(self):
        text_a = "aaa"
        text_b = "bbb"
        Item.objects.create(text=text_a)
        Item.objects.create(text=text_b)

        response = self.client.get("/")

        self.assertIn(text_a, response.content.decode())
        self.assertIn(text_b, response.content.decode())


class ListViewTest(TestCase):
    def test_displays_all_items(self):
        text_a = "aaa"
        text_b = "bbb"
        Item.objects.create(text=text_a)
        Item.objects.create(text=text_b)

        response = self.client.get("/lists/the-only-list-in-the-world/")

        self.assertContains(response, text_a)
        self.assertContains(response, text_b)


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
