from unittest import skip

from selenium.webdriver.common.keys import Keys

from functional_tests.base import FunctionalTest


class ItemValidationTest(FunctionalTest):
    def test_cannot_add_empty_list_items(self):
        # User goes to the home page and tries to submit an empty list item.
        # i.e. hits enter on an empty input box
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_id("id_new_item").send_keys(Keys.ENTER)

        # The home page refreshes with an error message
        self.assertEqual("You can't have an empty list item", self.browser.find_element_by_css_selector(".has-error").text)

        # The user tries again with some text, which now works
        self.fail("Finish test")

        # Perversely, the user now tries again with an empty list item

        # And gets a similar error message

        # Which is correctable via adding input text
