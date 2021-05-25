import unittest

from selenium import webdriver


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
        self.fail("Finish the test!")

        # The user is invited to enter a to-do immediately

        # She enters "Buy peacock feathers" into a text box

        # She hits enter, the page updates, and now lists:
        # "1: Buy peacock feathers" as a to-do list item

        # There is still a text box to enter another item.  She
        # enters "Use peacock feathers to make a fly"

        # The page updates again, and now shows both items

        # There is now a unique URL to use to save her to-do list
        # There is explanatory text to that effect.

        # The user visits that unique URL and the todo list is still there!


if __name__ == "__main__":
    unittest.main(warnings="ignore")
