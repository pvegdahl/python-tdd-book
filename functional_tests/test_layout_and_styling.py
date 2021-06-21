from functional_tests.base import FunctionalTest


class LayoutAndStylingTest(FunctionalTest):
    def test_layout_and_styling(self):
        # Edith goes to the home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # She notices the input box is nicely centered
        input_box = self._get_input_box()
        self.assertAlmostEqual(
            512, input_box.location["x"] + input_box.size["width"] / 2, delta=10
        )

        # She starts a new list and the input box is nicely centered there too
        self._send_input("testing")
        self._wait_for_row_in_list_table("1: testing")
        input_box = self._get_input_box()
        self.assertAlmostEqual(
            512, input_box.location["x"] + input_box.size["width"] / 2, delta=10
        )
