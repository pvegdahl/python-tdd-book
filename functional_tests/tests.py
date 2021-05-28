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
        # Satisfied, she goes back to sleep
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

        # There is now a unique URL to use to save her to-do list
        # There is explanatory text to that effect.
        self.fail("Finish the test!")

        # The user visits that unique URL and the todo list is still there!

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
