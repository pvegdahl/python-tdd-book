import os

from functional_tests.base import FunctionalTest
from functional_tests.management.commands.create_session import (
    create_preauthenticated_session,
)
from functional_tests.server_tools import create_session_on_server
from superlists import settings

EMAIL = "bob@builder.the"


class MyListsTest(FunctionalTest):
    def test_pre_authenticated_session(self):
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_out(EMAIL)

        self._create_pre_authenticated_session(EMAIL)
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_in(EMAIL)

    def _create_pre_authenticated_session(self, email: str):
        if self.staging_server:
            session_key = create_session_on_server(
                user=os.environ.get("USER"), host=self.staging_server, email=email
            )
        else:
            session_key = create_preauthenticated_session(email)

        # To set a cookie, we first need to visit the domain.  404 pages load the quickest ;-)
        self.browser.get(f"{self.live_server_url}/404_no_such_url/")
        self.browser.add_cookie(
            dict(name=settings.SESSION_COOKIE_NAME, value=session_key, path="/")
        )

    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        # Pre-log in
        self._create_pre_authenticated_session(EMAIL)

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
