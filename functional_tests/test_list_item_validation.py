from selenium.webdriver.common.keys import Keys

from functional_tests.base import FunctionalTest


class ItemValidationTest(FunctionalTest):
    def test_cannot_add_empty_list_items(self):
        # User goes to the home page and tries to submit an empty list item.
        # i.e. hits enter on an empty input box
        self.browser.get(self.live_server_url)
        self._get_input_box().send_keys(Keys.ENTER)

        # the browser intercepts the request, and does not load the list page
        self._wait_for(
            lambda: self.browser.find_element_by_css_selector("#id_text:invalid")
        )

        # The user starts typing, and the error disappears
        self._get_input_box().send_keys("Write test")
        self._wait_for(
            lambda: self.browser.find_element_by_css_selector("#id_text:valid")
        )

        # And the user can submit it successfully
        self._get_input_box().send_keys(Keys.ENTER)
        self._wait_for_row_in_list_table("1: Write test")

        # Perversely, the user now tries again with an empty list item
        self._get_input_box().send_keys(Keys.ENTER)

        # And again the browser will not comply
        self._wait_for_row_in_list_table("1: Write test")
        self._wait_for(
            lambda: self.browser.find_element_by_css_selector("#id_text:invalid")
        )

        # Which is correctable via adding input text
        self._get_input_box().send_keys("Make test pass")
        self._wait_for(
            lambda: self.browser.find_element_by_css_selector("#id_text:valid")
        )

        self._get_input_box().send_keys(Keys.ENTER)
        self._wait_for_row_in_list_table("2: Make test pass")
        self._send_input("Refactor")
        self._wait_for_row_in_list_table("1: Write test")
        self._wait_for_row_in_list_table("2: Make test pass")
        self._wait_for_row_in_list_table("3: Refactor")

    def test_cannot_add_duplicate_items(self):
        # Go to the home page and start a new list
        self.browser.get(self.live_server_url)
        input_text = "Not so unique input"
        self._send_input(input_text)
        self._wait_for_row_in_list_table(f"1: {input_text}")

        # Attempt to add a duplicate item
        self._send_input(input_text)

        # See a helpful error message
        self._assert_error_message_for_duplicates()
        self._wait_for_row_in_list_table(f"1: {input_text}")
        self.assertNotIn(
            f"2: {input_text}",
            [
                row.text
                for row in self.browser.find_element_by_id(
                    "id_list_table"
                ).find_elements_by_tag_name("tr")
            ],
        )

    def _assert_error_message_for_duplicates(self):
        self._wait_for(
            lambda: self.assertEqual(
                "You've already got this in your list",
                self._get_error_element().text,
            )
        )

    def _get_error_element(self):
        return self.browser.find_element_by_css_selector(".has-error")

    def test_error_messages_are_cleared_on_input(self):
        # Start a list and cause a dup validation error
        self.browser.get(self.live_server_url)
        duplicate_text = "Banter too thick"
        self._send_input(duplicate_text)
        self._wait_for_row_in_list_table(f"1: {duplicate_text}")
        self._send_input(duplicate_text)

        self._wait_for(lambda: self.assertTrue(self._get_error_element().is_displayed()))

        # Typing in the input box clears the error
        self._get_input_box().send_keys("a")

        self._wait_for(lambda: self.assertFalse(self._get_error_element().is_displayed()))

