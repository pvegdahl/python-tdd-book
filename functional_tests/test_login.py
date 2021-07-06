import re
import time

import poplib
import os

from django.core import mail
from selenium.webdriver.common.keys import Keys

from accounts.views import EMAIL_SUBJECT
from functional_tests.base import FunctionalTest


class LoginTest(FunctionalTest):
    def test_can_get_email_link_to_log_in(self):
        # Go to the (awesome) superlists site.
        # Notice the new login section and enter email address
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_name("email").send_keys(self.get_test_email())
        self.browser.find_element_by_name("email").send_keys(Keys.ENTER)

        # A message appears telling the user an email has been sent
        self.wait_for(
            lambda: self.assertIn(
                "Check your email", self.browser.find_element_by_tag_name("body").text
            )
        )

        # Check email and find a message
        email_body = self.wait_for_email(EMAIL_SUBJECT)

        # The email has a url link in it
        self.assertIn("Use this link to log in", email_body)
        url_search = re.search(r"http://.+/.+$", email_body)
        if not url_search:
            self.fail(f"Could not find URL in email body:\n{email_body}")
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # Click it!
        self.browser.get(url)

        # The user is logged in!
        self.wait_to_be_logged_in(self.get_test_email())

        # Now log back out
        self.browser.find_element_by_link_text("Log out").click()

        # And assert that it worked
        self.wait_to_be_logged_out(self.get_test_email())

    def get_test_email(self):
        if self.staging_server:
            return os.environ.get("TEST_EMAIL_ADDRESS")
        else:
            return "edith@example.com"

    def wait_for_email(self, subject) -> str:
        if not self.staging_server:
            email = mail.outbox[0]
            self.assertIn(self.get_test_email(), email.to)
            self.assertEqual(email.subject, subject)
            return email.body

        email_id = None
        start_time = time.time()
        inbox = poplib.POP3_SSL("pop.gmail.com")
        try:
            inbox.user(self.get_test_email())
            inbox.pass_(os.environ.get("TEST_EMAIL_PASSWORD"))
            while time.time() - start_time < 60:
                # Get 10 newest messages
                count, _ = inbox.stat()
                for i in reversed(range(max(1, count - 10), count + 1)):
                    print(f"Getting message {i}")
                    _, lines, __ = inbox.retr(i)
                    lines = [line.decode("utf8") for line in lines]
                    print(lines)
                    if f"Subject: {subject}" in lines:
                        email_id = i
                        body = "\n".join(lines)
                        return body
                    time.sleep(5)
        finally:
            if email_id:
                inbox.dele(email_id)
            inbox.quit()
