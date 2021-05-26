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

        table = self.browser.find_element_by_id("id_list_table")
        rows = table.find_elements_by_tag_name("tr")
        self.assertTrue(any(row.text == "1: Buy peacock feathers" for row in rows))

        # There is still a text box to enter another item.  She
        # enters "Use peacock feathers to make a fly"
        self.fail("Finish the test!")

        # The page updates again, and now shows both items

        # There is now a unique URL to use to save her to-do list
        # There is explanatory text to that effect.

        # The user visits that unique URL and the todo list is still there!


if __name__ == "__main__":
    unittest.main(warnings="ignore")
