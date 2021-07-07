import os

from functional_tests.base import FunctionalTest
from functional_tests.management.commands.create_session import create_preauthenticated_session
from functional_tests.server_tools import create_session_on_server
from superlists import settings

EMAIL = "bob@builder.the"


class MyListsTest(FunctionalTest):
    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_out(EMAIL)

        self.create_pre_authenticated_session(EMAIL)
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_in(EMAIL)

    def create_pre_authenticated_session(self, email: str):
        if self.staging_server:
            session_key = create_session_on_server(user=os.environ.get("USER"), host=self.staging_server, email=email)
        else:
            session_key = create_preauthenticated_session(email)

        # To set a cookie, we first need to visit the domain.  404 pages load the quickest ;-)
        self.browser.get(f"{self.live_server_url}/404_no_such_url/")
        self.browser.add_cookie(
            dict(name=settings.SESSION_COOKIE_NAME, value=session_key, path="/")
        )
