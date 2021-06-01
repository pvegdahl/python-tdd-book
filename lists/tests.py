from django.test import TestCase
from lists.models import Item, List


class HomePageTest(TestCase):
    def test_homepage_returns_correct_html(self):
        self.assertTemplateUsed(self.client.get("/"), "home.html")


class ListViewTest(TestCase):
    def test_displays_all_items(self):
        list_ = List.objects.create()
        text_a = "aaa"
        text_b = "bbb"
        Item.objects.create(text=text_a, list=list_)
        Item.objects.create(text=text_b, list=list_)

        response = self.client.get("/lists/the-only-list-in-the-world/")

        self.assertContains(response, text_a)
        self.assertContains(response, text_b)

    def test_use_list_template(self):
        self.assertTemplateUsed(self.client.get("/lists/the-only-list-in-the-world/"), "list.html")


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
        self.assertRedirects(response, "/lists/the-only-list-in-the-world/")

