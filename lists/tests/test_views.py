from django.test import TestCase
from django.utils.html import escape

from lists.forms import ItemForm
from lists.models import Item, List


class HomePageTest(TestCase):
    def test_homepage_uses_correct_template(self):
        self.assertTemplateUsed(self.client.get("/"), "home.html")

    def test_home_page_uses_item_form(self):
        self.assertIsInstance(self.client.get("/").context["form"], ItemForm)


class ListViewTest(TestCase):
    def test_use_list_template(self):
        the_list = List.objects.create()
        self.assertTemplateUsed(self.client.get(f"/lists/{the_list.id}/"), "list.html")

    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        text_a = "itemy 1"
        text_b = "itemy 2"
        Item.objects.create(text=text_a, list=correct_list)
        Item.objects.create(text=text_b, list=correct_list)

        other_list = List.objects.create()
        other_text_a = "other text 1"
        other_text_b = "other text 2"
        Item.objects.create(text=other_text_a, list=other_list)
        Item.objects.create(text=other_text_b, list=other_list)

        response = self.client.get(f"/lists/{correct_list.id}/")

        self.assertContains(response, text_a)
        self.assertContains(response, text_b)
        self.assertNotContains(response, other_text_a)
        self.assertNotContains(response, other_text_b)

    def test_passes_correct_list_to_template(self):
        List.objects.create()  # other list
        correct_list = List.objects.create()
        response = self.client.get(f"/lists/{correct_list.id}/")
        self.assertEqual(correct_list, response.context["list"])

    def test_can_save_a_POST_request_to_an_existing_list(self):
        List.objects.create()  # Other list
        correct_list = List.objects.create()

        correct_item_text = "A new item for an existing list"
        self.client.post(
            f"/lists/{correct_list.id}/", data={"item_text": correct_item_text}
        )

        self.assertEqual(1, Item.objects.count())
        new_item = Item.objects.first()
        self.assertEqual(correct_item_text, new_item.text)
        self.assertEqual(correct_list, new_item.list)

    def test_POST_redirects_to_list_view(self):
        List.objects.create()  # Other list
        correct_list = List.objects.create()

        response = self.client.post(
            f"/lists/{correct_list.id}/", data={"item_text": "irrelevant text"}
        )

        self.assertRedirects(response, f"/lists/{correct_list.id}/")

    def test_validation_errors_end_up_on_lists_page(self):
        the_list = List.objects.create()
        response = self.client.post(f"/lists/{the_list.id}/", data={"item_text": ""})
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, "list.html")
        self.assertContains(response, escape("You can't have an empty list item"))


class NewListTest(TestCase):
    def test_can_save_a_post_request(self):
        item_text = "A new list item"
        self.client.post("/lists/new", data={"item_text": item_text})
        self.assertEqual(1, Item.objects.count())
        self.assertEqual(item_text, Item.objects.first().text)

    def test_redirects_after_post(self):
        response = self.client.post("/lists/new", data={"item_text": "The item text"})
        new_list = List.objects.first()
        self.assertRedirects(response, f"/lists/{new_list.id}/")

    def test_validation_errors_are_sent_back_to_homepage_template(self):
        response = self.client.post("/lists/new", data={"item_text": ""})
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, "home.html")
        self.assertContains(response, escape("You can't have an empty list item"))

    def test_invalid_list_items_are_not_saved(self):
        self.client.post("/lists/new", data={"item_text": ""})
        self.assertEqual(0, List.objects.count())
        self.assertEqual(0, Item.objects.count())
