from django.test import TestCase

from lists.forms import ItemForm, EMPTY_ITEM_ERROR


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
            item_form.save()
