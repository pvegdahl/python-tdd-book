from django.contrib.auth import SESSION_KEY, BACKEND_SESSION_KEY
from django.contrib.sessions.backends.db import SessionStore

from accounts.models import User
from functional_tests.base import FunctionalTest
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
        user = User.objects.create(email=email)
        session = SessionStore()
        session[SESSION_KEY] = user.pk
        session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
        session.save()

        # To set a cookie, we first need to visit the domain.  404 pages load the quickest ;-)
        self.browser.get(f"{self.live_server_url}/404_no_such_url/")
        self.browser.add_cookie(
            dict(name=settings.SESSION_COOKIE_NAME, value=session.session_key, path="/")
        )
