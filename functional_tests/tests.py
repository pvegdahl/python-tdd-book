import time
import unittest

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase


class NewVisitorTest(LiveServerTestCase):
    def setUp(self) -> None:
        self.browser = webdriver.Firefox()

    def tearDown(self) -> None:
        # Satisfied, everyone goes back to sleep
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Go to the webpage to check out the app
        self.browser.get(self.live_server_url)

        # The page title mentions to-do lists
        self.assertIn("To-Do", self.browser.title)
        header_text = self.browser.find_element_by_tag_name("h1").text
        self.assertIn("To-Do", header_text)

        # The user is invited to enter a to-do immediately
        input_box = self.browser.find_element_by_id("id_new_item")
        self.assertEqual("Enter a to-do item", input_box.get_attribute("placeholder"))

        # She enters "Buy peacock feathers" into a text box
        # She hits enter, the page updates, and now lists:
        # "1: Buy peacock feathers" as a to-do list item
        self._send_input("Buy peacock feathers")

        self._wait_for_row_in_list_table("1: Buy peacock feathers")

        # There is still a text box to enter another item.  She
        # enters "Use peacock feathers to make a fly"
        self._send_input("Use peacock feathers to make a fly")

        # The page updates again, and now shows both items
        self._wait_for_row_in_list_table("1: Buy peacock feathers")
        self._wait_for_row_in_list_table("2: Use peacock feathers to make a fly")


    def _wait_for_row_in_list_table(self, row_text: str, timeout: int = 5) -> None:
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id("id_list_table")
                rows = table.find_elements_by_tag_name("tr")
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > timeout:
                    raise e
                time.sleep(0.1)

    def _send_input(self, input_text: str) -> None:
        input_box = self.browser.find_element_by_id("id_new_item")
        input_box.send_keys(input_text)
        input_box.send_keys(Keys.ENTER)

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Edith starts a new to-do list
        self.browser.get(self.live_server_url)
        self._send_input("Buy peacock feathers")
        self._wait_for_row_in_list_table("1: Buy peacock feathers")

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
        self._send_input("Buy milk")
        self._wait_for_row_in_list_table("1: Buy milk")

        # Francis gets his own URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, "/lists/.+")
        self.assertNotEqual(francis_list_url, edith_list_url)

        # Again, there is no trace of edith's list
        page_text = self.browser.find_element_by_tag_name("body").text
        self.assertNotIn("Buy peacock feathers", page_text)
        self.assertNotIn("make a fly", page_text)