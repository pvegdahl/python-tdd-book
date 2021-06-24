from unittest import skip

from django.test import TestCase
from django.utils.html import escape

from lists.forms import ItemForm, EMPTY_ITEM_ERROR
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
            f"/lists/{correct_list.id}/", data={"text": correct_item_text}
        )

        self.assertEqual(1, Item.objects.count())
        new_item = Item.objects.first()
        self.assertEqual(correct_item_text, new_item.text)
        self.assertEqual(correct_list, new_item.list)

    def test_POST_redirects_to_list_view(self):
        List.objects.create()  # Other list
        correct_list = List.objects.create()

        response = self.client.post(
            f"/lists/{correct_list.id}/", data={"text": "irrelevant text"}
        )

        self.assertRedirects(response, f"/lists/{correct_list.id}/")

    def test_for_invalid_input_nothing_saved_to_db(self):
        self._post_invalid_input()
        self.assertEqual(0, Item.objects.count())

    def _post_invalid_input(self):
        the_list = List.objects.create()
        return self.client.post(f"/lists/{the_list.id}/", data={"text": ""})

    def test_for_invalid_input_renders_list_template(self):
        response = self._post_invalid_input()
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, "list.html")

    def test_for_invalid_input_passes_form_to_template(self):
        response = self._post_invalid_input()
        self.assertIsInstance(response.context["form"], ItemForm)

    def test_for_invalid_input_shows_error_on_page(self):
        response = self._post_invalid_input()
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    def test_displays_item_form(self):
        the_list = List.objects.create()
        response = self.client.get(f"/lists/{the_list.id}/")
        self.assertIsInstance(response.context["form"], ItemForm)
        self.assertContains(response, 'name="text"')

    @skip
    def test_invalid_duplicate_input_shows_error_on_page(self):
        list_1 = List.objects.create()
        duplicate_text = "knock knock"
        item_1 = Item.objects.create(list=list_1, text=duplicate_text)
        response = self.client.post(f"/lists/{list_1.id}/", data={"text": duplicate_text})

        expected_error = escape("You've already got this in your list")
        self.assertContains(response, expected_error)
        self.assertTemplateUsed(response, "list.html")
        self.assertEqual([item_1], list(Item.objects.all()))


class NewListTest(TestCase):
    def test_can_save_a_post_request(self):
        item_text = "A new list item"
        self.client.post("/lists/new", data={"text": item_text})
        self.assertEqual(1, Item.objects.count())
        self.assertEqual(item_text, Item.objects.first().text)

    def test_redirects_after_post(self):
        response = self.client.post("/lists/new", data={"text": "The item text"})
        new_list = List.objects.first()
        self.assertRedirects(response, f"/lists/{new_list.id}/")

    def test_invalid_list_items_are_not_saved(self):
        self.client.post("/lists/new", data={"text": ""})
        self.assertEqual(0, List.objects.count())
        self.assertEqual(0, Item.objects.count())

    def test_invalid_input_renders_home_template(self):
        response = self.client.post("/lists/new", data={"text": ""})
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, "home.html")

    def test_validation_errors_are_shown_on_home_page(self):
        response = self.client.post("/lists/new", data={"text": ""})
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    def test_invalid_input_passes_form_to_template(self):
        response = self.client.post("/lists/new", data={"text": ""})
        self.assertIsInstance(response.context["form"], ItemForm)
