from functional_tests.base import FunctionalTest, wait


class LayoutAndStylingTest(FunctionalTest):
    def test_layout_and_styling(self):
        # Edith goes to the home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # She notices the input box is nicely centered
        self._assert_input_box_is_centered()

        # She starts a new list and the input box is nicely centered there too
        self.add_list_item("testing")
        self.wait_for_row_in_list_table("1: testing")
        self._assert_input_box_is_centered()

    @wait
    def _assert_input_box_is_centered(self):
        self.assertAlmostEqual(
            512,
            self.get_input_box().location["x"] + self.get_input_box().size["width"] / 2,
            delta=10,
        )
