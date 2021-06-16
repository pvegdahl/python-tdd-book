from django.test import TestCase
from lists.models import Item, List


class ListAndItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()

        first_text = "The first (ever) list item"
        first_item = Item()
        first_item.text = first_text
        first_item.list = list_
        first_item.save()

        second_text = "Item the second"
        second_item = Item()
        second_item.text = second_text
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(list_, saved_list)

        saved_items = Item.objects.all()
        self.assertEqual(2, len(saved_items))

        self.assertEqual(first_text, saved_items[0].text)
        self.assertEqual(list_, saved_items[0].list)
        self.assertEqual(second_text, saved_items[1].text)
        self.assertEqual(list_, saved_items[1].list)
