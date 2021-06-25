from django.test import TestCase

from lists.forms import (
    ItemForm,
    EMPTY_ITEM_ERROR,
    ExistingListItemForm,
    DUPLICATE_ITEM_ERROR,
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
