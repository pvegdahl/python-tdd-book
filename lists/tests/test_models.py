from django.core.exceptions import ValidationError
from django.test import TestCase

from accounts.models import User
from lists.models import Item, List


class ItemModelTest(TestCase):
    def test_default_text(self):
        self.assertEqual("", Item().text)

    def test_item_is_related_to_list(self):
        the_list = List.objects.create()
        item_1 = Item(text="whatever", list=the_list)
        item_1.save()
        item_2 = Item(text="whatever else", list=the_list)
        item_2.save()
        self.assertEqual([item_1, item_2], list(the_list.item_set.all()))

    def test_cannot_save_empty_items(self):
        the_list = List.objects.create()
        item = Item(list=the_list, text="")
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

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


class ListModelTest(TestCase):
    def test_get_absolute_url(self):
        the_list = List.objects.create()
        self.assertEqual(f"/lists/{the_list.id}/", the_list.get_absolute_url())

    def test_create_new_creates_list_and_first_item(self):
        item_text = "Some text for the item"
        List.create_new(first_item_text=item_text)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, item_text)
        self.assertEqual(List.objects.first(), new_item.list)

    def test_create_new_optionally_saves_owner(self):
        user = User.objects.create()
        List.create_new(first_item_text="Text text text", owner=user)
        self.assertEqual(List.objects.first().owner, user)

    @staticmethod
    def test_lists_can_have_owners():
        List(owner=User())  # Should not raise

    @staticmethod
    def test_list_owners_are_optional():
        List().full_clean()  # Should not raise

    def test_create_new_returns_list(self):
        result = List.create_new("the text")
        self.assertEqual(List.objects.first(), result)

    def test_list_name_is_first_item_text(self):
        first_item_text = "Un"
        the_list = List.objects.create()
        Item.objects.create(text=first_item_text, list=the_list)
        Item.objects.create(text="Deux", list=the_list)
        self.assertEqual(the_list.name, first_item_text)

    def test_empty_list_has_name_Empty_List(self):
        the_list = List.objects.create()
        self.assertEqual(the_list.name, "Empty List")
