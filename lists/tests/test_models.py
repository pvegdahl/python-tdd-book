from django.core.exceptions import ValidationError
from django.test import TestCase
from lists.models import Item, List


class ListAndItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        the_list = List()
        the_list.save()

        first_text = "The first (ever) list item"
        first_item = Item()
        first_item.text = first_text
        first_item.list = the_list
        first_item.save()

        second_text = "Item the second"
        second_item = Item()
        second_item.text = second_text
        second_item.list = the_list
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(the_list, saved_list)

        saved_items = Item.objects.all()
        self.assertEqual(2, len(saved_items))

        self.assertEqual(first_text, saved_items[0].text)
        self.assertEqual(the_list, saved_items[0].list)
        self.assertEqual(second_text, saved_items[1].text)
        self.assertEqual(the_list, saved_items[1].list)

    def test_cannot_save_empty_items(self):
        the_list = List.objects.create()
        item = Item(list=the_list, text="")
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_get_absolute_url(self):
        the_list = List.objects.create()
        self.assertEqual(f"/lists/{the_list.id}/", the_list.get_absolute_url())

    def test_duplicate_items_are_invalid(self):
        the_list = List.objects.create()
        text = "Duplicate text"
        Item.objects.create(text=text, list=the_list)
        with self.assertRaises(ValidationError):
            item = Item(text=text, list=the_list)
            item.full_clean()

    @staticmethod
    def test_CAN_save_duplicate_items_to_different_lists():
        list_1 = List.objects.create()
        text = "Duplicate text"
        Item.objects.create(text=text, list=list_1)

        list_2 = List.objects.create()
        item = Item(text=text, list=list_2)
        item.full_clean()  # Should not raise an exception

    def test_list_ordering(self):
        the_list = List.objects.create()
        item_1 = Item.objects.create(list=the_list, text="one")
        item_2 = Item.objects.create(list=the_list, text="two")
        item_3 = Item.objects.create(list=the_list, text="three")
        self.assertEqual([item_1, item_2, item_3], list(Item.objects.all()))

    def test_item_string_representation(self):
        text = "some text"
        item = Item(text=text)
        self.assertEqual(text, str(item))

