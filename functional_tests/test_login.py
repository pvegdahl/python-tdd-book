import re

from django.core import mail
from selenium.webdriver.common.keys import Keys

from accounts.views import EMAIL_SUBJECT
from functional_tests.base import FunctionalTest

TEST_EMAIL = "edith@example.com"


class LoginTest(FunctionalTest):
    def test_can_get_email_link_to_log_in(self):
        # Go to the (awesome) superlists site.
        # Notice the new login section and enter email address
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_name("email").send_keys(TEST_EMAIL)
        self.browser.find_element_by_name("email").send_keys(Keys.ENTER)

        # A message appears telling the user an email has been sent
        self._wait_for(
            lambda: self.assertIn(
                "Check your email", self.browser.find_element_by_tag_name("body").text
            )
        )

        # Check email and find a message
        email = mail.outbox[0]
        self.assertIn(TEST_EMAIL, email.to)
        self.assertEqual(email.subject, EMAIL_SUBJECT)

        # The email has a url link in it
        self.assertIn("Use this link to log in", email.body)
        url_search = re.search(r"http://.+/.+$", email.body)
        if not url_search:
            self.fail(f"Could not find URL in email body:\n{email.body}")
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # Click it!
        self.browser.get(url)

        # The user is logged in!
        self.wait_to_be_logged_in(TEST_EMAIL)

        # Now log back out
        self.browser.find_element_by_link_text("Log out").click()

        # And assert that it worked
        self.wait_to_be_logged_out(TEST_EMAIL)
