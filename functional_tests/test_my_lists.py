from functional_tests.base import FunctionalTest

EMAIL = "bob@builder.the"


class MyListsTest(FunctionalTest):
    def test_pre_authenticated_session(self):
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_out(EMAIL)

        self.create_pre_authenticated_session(EMAIL)
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_in(EMAIL)

    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        # Pre-log in
        self.create_pre_authenticated_session(EMAIL)

        # Go to the home page and start a list
        self.browser.get(self.live_server_url)
        item_1 = "Write the test"
        self.add_list_item(item_1)
        self.add_list_item("Write the code")
        first_list_url = self.browser.current_url

        # The user sees and clicks a "My lists" link
        self.browser.find_element_by_link_text("My lists").click()

        # And the new list is there, named after the first item on the list
        self.wait_for(lambda: self.browser.find_element_by_link_text(item_1))
        self.browser.find_element_by_link_text(item_1).click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, first_list_url)
        )

        # Let's add another list
        self.browser.get(self.live_server_url)
        item_2 = "Click cows"
        self.add_list_item(item_2)
        second_list_url = self.browser.current_url

        # Under "My lists," the new list appears
        self.browser.find_element_by_link_text("My lists").click()
        self.wait_for(lambda: self.browser.find_element_by_link_text(item_2))
        self.browser.find_element_by_link_text(item_2).click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, second_list_url)
        )

        # After logging out, "My lists" disappears
        self.browser.find_element_by_link_text("Log out").click()
        self.wait_for(
            lambda: self.assertEqual(
                self.browser.find_elements_by_link_text("My lists"), []
            )
        )
