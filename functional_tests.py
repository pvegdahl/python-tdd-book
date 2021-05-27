import time
import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(unittest.TestCase):
    def setUp(self) -> None:
        self.browser = webdriver.Firefox()

    def tearDown(self) -> None:
        # Satisfied, she goes back to sleep
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Go to the webpage to check out the app
        self.browser.get("http://localhost:8000")

        # The page title mentions to-do lists
        self.assertIn("To-Do", self.browser.title)
        header_text = self.browser.find_element_by_tag_name("h1").text
        self.assertIn("To-Do", header_text)

        # The user is invited to enter a to-do immediately
        input_box = self.browser.find_element_by_id("id_new_item")
        self.assertEqual("Enter a to-do item", input_box.get_attribute("placeholder"))

        # She enters "Buy peacock feathers" into a text box
        input_box.send_keys("Buy peacock feathers")

        # She hits enter, the page updates, and now lists:
        # "1: Buy peacock feathers" as a to-do list item
        input_box.send_keys(Keys.ENTER)
        time.sleep(1)

        self._check_for_row_in_list_table("1: Buy peacock feathers")

        # There is still a text box to enter another item.  She
        # enters "Use peacock feathers to make a fly"
        input_box = self.browser.find_element_by_id("id_new_item")
        input_box.send_keys("Use peacock feathers to make a fly")
        input_box.send_keys(Keys.ENTER)
        time.sleep(1)

        # The page updates again, and now shows both items
        table = self.browser.find_element_by_id("id_list_table")
        rows = table.find_elements_by_tag_name("tr")
        self._check_for_row_in_list_table("1: Buy peacock feathers")
        self._check_for_row_in_list_table("2: Use peacock feathers to make a fly")

        # There is now a unique URL to use to save her to-do list
        # There is explanatory text to that effect.
        self.fail("Finish the test!")

        # The user visits that unique URL and the todo list is still there!

    def _check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id("id_list_table")
        rows = table.find_elements_by_tag_name("tr")
        self.assertIn(row_text, [row.text for row in rows])



if __name__ == "__main__":
    unittest.main(warnings="ignore")
