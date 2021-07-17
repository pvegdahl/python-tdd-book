from unittest.mock import patch, Mock
import unittest

from django.http import HttpRequest
from django.test import TestCase
from django.utils.html import escape

from accounts.models import User
from lists.forms import (
    ItemForm,
    EMPTY_ITEM_ERROR,
    DUPLICATE_ITEM_ERROR,
    ExistingListItemForm,
)
from lists.models import Item, List
from lists.views import new_list, share_list

EMAIL = "daffy@duck.com"


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
        self.client.post(f"/lists/{correct_list.id}/", data={"text": correct_item_text})

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
        self.assertIsInstance(response.context["form"], ExistingListItemForm)

    def test_for_invalid_input_shows_error_on_page(self):
        response = self._post_invalid_input()
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    def test_displays_item_form(self):
        the_list = List.objects.create()
        response = self.client.get(f"/lists/{the_list.id}/")
        self.assertIsInstance(response.context["form"], ExistingListItemForm)
        self.assertContains(response, 'name="text"')

    def test_invalid_duplicate_input_shows_error_on_page(self):
        list_1 = List.objects.create()
        duplicate_text = "knock knock"
        item_1 = Item.objects.create(list=list_1, text=duplicate_text)
        response = self.client.post(
            f"/lists/{list_1.id}/", data={"text": duplicate_text}
        )

        self.assertContains(response, escape(DUPLICATE_ITEM_ERROR))
        self.assertTemplateUsed(response, "list.html")
        self.assertEqual([item_1], list(Item.objects.all()))


class NewListViewIntegratedTest(TestCase):
    def test_can_save_a_post_request(self):
        item_text = "A new list item"
        self.client.post("/lists/new", data={"text": item_text})
        self.assertEqual(1, Item.objects.count())
        self.assertEqual(item_text, Item.objects.first().text)

    def test_invalid_list_items_are_not_saved_and_error_is_shown_on_homepage(self):
        response = self.client.post("/lists/new", data={"text": ""})
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))
        self.assertEqual(0, List.objects.count())
        self.assertEqual(0, Item.objects.count())

    def test_list_owner_is_saved_if_user_is_authenticated(self):
        user = User.objects.create(email=EMAIL)
        self.client.force_login(user)

        self.client.post("/lists/new", data={"text": "the content"})

        the_list = List.objects.first()
        self.assertEqual(the_list.owner, user)


@patch("lists.views.NewListForm")
class NewListViewTests(unittest.TestCase):
    def setUp(self):
        self.request = HttpRequest()
        self.request.POST["text"] = "new list item"
        self.request.user = Mock()

    def test_passes_POST_data_to_NewListForm(self, mock_new_list_form):
        new_list(self.request)
        mock_new_list_form.assert_called_once_with(data=self.request.POST)

    def test_saves_form_with_owner_if_valid(self, mock_new_list_form):
        mock_form = mock_new_list_form.return_value
        mock_form.is_valid.return_value = True
        new_list(self.request)
        mock_form.save.assert_called_once_with(owner=self.request.user)

    @patch("lists.views.redirect")
    def test_redirects_to_form_returned_object_if_valid(
        self, mock_redirect, mock_new_list_form
    ):
        mock_form = mock_new_list_form.return_value
        mock_form.is_valid.return_value = True

        response = new_list(self.request)

        self.assertEqual(response, mock_redirect.return_value)
        mock_redirect.assert_called_once_with(mock_form.save.return_value)

    @patch("lists.views.render")
    def test_renders_home_page_if_form_is_invalid(
        self, mock_render, mock_new_list_form
    ):
        mock_form = mock_new_list_form.return_value
        mock_form.is_valid.return_value = False

        response = new_list(self.request)

        self.assertEqual(response, mock_render.return_value)
        mock_render.assert_called_once_with(
            self.request, "home.html", {"form": mock_form}
        )

    def test_form_does_not_save_if_list_is_invalid(self, mock_new_list_form):
        mock_form = mock_new_list_form.return_value
        mock_form.is_valid.return_value = False

        new_list(self.request)

        mock_form.save.assert_not_called()


class MyListsTest(TestCase):
    def test_my_lists_url_renders_my_lists_template(self):
        User.objects.create(email=EMAIL)
        response = self.client.get(f"/lists/users/{EMAIL}/")
        self.assertTemplateUsed(response, "my_lists.html")

    def test_passes_correct_owner_to_template(self):
        User.objects.create(email="wrong@owner.com")
        correct_user = User.objects.create(email=EMAIL)
        response = self.client.get(f"/lists/users/{EMAIL}/")
        self.assertEqual(response.context["owner"], correct_user)


class ShareListTest(TestCase):
    def test_POST_redirects_to_list_page(self):
        the_list = List.objects.create()
        response = self.client.post(
            f"/lists/{the_list.id}/share"  #, data={"email": "some@email.com"}
        )
        self.assertRedirects(response, f"/lists/{the_list.id}/")
