from unittest import skip

from functional_tests.base import FunctionalTest


class ItemValidationTest(FunctionalTest):
    @skip
    def test_cannot_add_empty_list_items(self):
        # User goes to the home page and tries to submit an empty list item.
        # i.e. hits enter on an empty input box

        # The home page refreshes with an error message

        # The user tries again with some text, which now works

        # Perversely, the user now tries again with an empty list item

        # And gets a similar error message

        # Which is correctable via adding input text
        self.fail("Finish test")