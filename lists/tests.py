from django.test import TestCase
from lists.models import Item, List


class HomePageTest(TestCase):
    def test_homepage_returns_correct_html(self):
        self.assertTemplateUsed(self.client.get("/"), "home.html")


class ListViewTest(TestCase):
    def test_use_list_template(self):
        list_ = List.objects.create()
        self.assertTemplateUsed(self.client.get(f"/lists/{list_.id}/"), "list.html")

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

