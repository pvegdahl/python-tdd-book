from functional_tests.base import FunctionalTest


class ItemValidationTest(FunctionalTest):
    def test_cannot_add_empty_list_items(self):
        # User goes to the home page and tries to submit an empty list item.
        # i.e. hits enter on an empty input box
        self.browser.get(self.live_server_url)
        self._send_input("")

        # The home page refreshes with an error message
        self._assert_error_message()

        # The user tries again with some text, which now works
        self._send_input("Write test")
        self._wait_for_row_in_list_table("1: Write test")

        # Perversely, the user now tries again with an empty list item
        self._send_input("")

        # And gets a similar error message
        self._assert_error_message()

        # Which is correctable via adding input text
        self._send_input("Make test pass")
        self._send_input("Refactor")
        self._wait_for_row_in_list_table("1: Write test")
        self._wait_for_row_in_list_table("2: Make test pass")
        self._wait_for_row_in_list_table("3: Refactor")

    def _assert_error_message(self):
        self._wait_for(
            lambda: self.assertEqual(
                "You can't have an empty list item",
                self.browser.find_element_by_css_selector(".has-error").text,
            )
        )
