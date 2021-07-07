from selenium import webdriver

from functional_tests.base import FunctionalTest


class NewVisitorTest(FunctionalTest):
    def test_can_start_a_list_for_one_user(self):
        # Go to the webpage to check out the app
        self.browser.get(self.live_server_url)

        # The page title mentions to-do lists
        self.assertIn("To-Do", self.browser.title)
        header_text = self.browser.find_element_by_tag_name("h1").text
        self.assertIn("To-Do", header_text)

        # The user is invited to enter a to-do immediately
        self.assertEqual(
            "Enter a to-do item", self.get_input_box().get_attribute("placeholder")
        )

        # She enters "Buy peacock feathers" into a text box
        # She hits enter, the page updates, and now lists:
        # "1: Buy peacock feathers" as a to-do list item
        self.add_list_item("Buy peacock feathers")

        self.wait_for_row_in_list_table("1: Buy peacock feathers")

        # There is still a text box to enter another item.  She
        # enters "Use peacock feathers to make a fly"
        self.add_list_item("Use peacock feathers to make a fly")

        # The page updates again, and now shows both items
        self.wait_for_row_in_list_table("1: Buy peacock feathers")
        self.wait_for_row_in_list_table("2: Use peacock feathers to make a fly")

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Edith starts a new to-do list
        self.browser.get(self.live_server_url)
        self.add_list_item("Buy peacock feathers")
        self.wait_for_row_in_list_table("1: Buy peacock feathers")

        # She notices that her list has a unique URL
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, "/lists/.+")

        # Now a new user, Francis, comes along to the site.

        # We use a new browser session to make sure that no information of Edith's is coming through from cookies, etc.
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Francis visits the home page.  There is no sign of Edith's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name("body").text
        self.assertNotIn("Buy peacock feathers", page_text)
        self.assertNotIn("make a fly", page_text)

        # Francis starts a new list by entering a new item.
        self.add_list_item("Buy milk")
        self.wait_for_row_in_list_table("1: Buy milk")

        # Francis gets his own URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, "/lists/.+")
        self.assertNotEqual(francis_list_url, edith_list_url)

        # Again, there is no trace of edith's list
        page_text = self.browser.find_element_by_tag_name("body").text
        self.assertNotIn("Buy peacock feathers", page_text)
        self.assertNotIn("make a fly", page_text)
