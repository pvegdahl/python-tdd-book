import unittest
from unittest.mock import patch, Mock

from django.test import TestCase

from lists.forms import (
    ItemForm,
    EMPTY_ITEM_ERROR,
    ExistingListItemForm,
    DUPLICATE_ITEM_ERROR,
    NewListForm,
)
from lists.models import List, Item


class ItemFormTest(TestCase):
    def test_form_item_has_placeholder_and_css_classes(self):
        item_form = ItemForm()
        self.assertIn('placeholder="Enter a to-do item"', item_form.as_p())
        self.assertIn('class="form-control input-lg"', item_form.as_p())

    def test_form_validation_for_blank_text(self):
        item_form = ItemForm(data={"text": ""})
        self.assertFalse(item_form.is_valid())
        self.assertEqual([EMPTY_ITEM_ERROR], item_form.errors["text"])

        with self.assertRaises(ValueError):
            item_form.save(for_list=None)

    def test_form_save_handles_saving_to_a_list(self):
        the_list = List.objects.create()
        form = ItemForm(data={"text": "valid text"})
        new_item = form.save(for_list=the_list)
        self.assertEqual(new_item, Item.objects.first())
        self.assertEqual("valid text", new_item.text)
        self.assertEqual(the_list, new_item.list)


class ExistingListItemFormTest(TestCase):
    def test_form_renders_item_text_input(self):
        the_list = List.objects.create()
        form = ExistingListItemForm(for_list=the_list)
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())

    def test_form_validation_for_blank_items(self):
        the_list = List.objects.create()
        form = ExistingListItemForm(for_list=the_list, data={"text": ""})
        self.assertFalse(form.is_valid())
        self.assertEqual([EMPTY_ITEM_ERROR], form.errors["text"])

    def test_form_validation_for_duplicate_items(self):
        the_list = List.objects.create()
        duplicate_text = "Twins!"
        Item.objects.create(list=the_list, text=duplicate_text)
        form = ExistingListItemForm(for_list=the_list, data={"text": duplicate_text})
        self.assertFalse(form.is_valid())
        self.assertEqual([DUPLICATE_ITEM_ERROR], form.errors["text"])

    def test_form_save(self):
        the_list = List.objects.create()
        form = ExistingListItemForm(for_list=the_list, data={"text": "hi"})
        new_item = form.save()
        self.assertEqual([new_item], list(Item.objects.all()))


class NewListFormTest(unittest.TestCase):
    @patch("lists.forms.List.create_new")
    def test_save_creates_new_list_from_post_data_if_user_not_authenticated(
        self, mock_list_create_new
    ):
        user = Mock(is_authenticated=False)
        input_text = "new item text"
        form = NewListForm(data={"text": input_text})
        form.is_valid()
        form.save(owner=user)
        mock_list_create_new.assert_called_once_with(first_item_text=input_text)

    @patch("lists.forms.List.create_new")
    def test_save_creates_new_list_from_post_data_if_user_authenticated(
        self, mock_list_create_new
    ):
        user = Mock(is_authenticated=True)
        input_text = "another new item text"
        form = NewListForm(data={"text": input_text})
        form.is_valid()
        form.save(owner=user)
        mock_list_create_new.assert_called_once_with(
            first_item_text=input_text, owner=user
        )

    @patch("lists.forms.List.create_new")
    def test_save_returns_new_list_object(self, mock_list_create_new):
        user = Mock(is_authenticated=True)
        input_text = "yet another new item text"
        form = NewListForm(data={"text": input_text})
        form.is_valid()
        result = form.save(owner=user)
        self.assertEqual(result, mock_list_create_new.return_value)
