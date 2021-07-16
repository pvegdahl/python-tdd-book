import os
import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys

from functional_tests.management.commands.create_session import create_preauthenticated_session
from functional_tests.server_tools import create_session_on_server
from superlists import settings


def wait(fn):
    max_wait = 5

    def modified_fn(*args, **kwargs):
        start_time = time.time()
        while True:
            try:
                return fn(*args, **kwargs)
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > max_wait:
                    raise e
                time.sleep(0.1)

    return modified_fn


class FunctionalTest(StaticLiveServerTestCase):
    def setUp(self) -> None:
        self.browser = webdriver.Firefox()
        self.staging_server = os.environ.get("STAGING_SERVER")
        if self.staging_server:
            # noinspection HttpUrlsUsage
            self.live_server_url = f"http://{self.staging_server}"

    def tearDown(self) -> None:
        # Satisfied, everyone goes back to sleep
        self.browser.quit()

    @wait
    def wait_for_row_in_list_table(self, row_text: str) -> None:
        self.assertIn(
            row_text,
            [
                row.text
                for row in (
                    self.browser.find_element_by_id(
                        "id_list_table"
                    ).find_elements_by_tag_name("tr")
                )
            ],
        )

    def add_list_item(self, input_text: str, validate: bool = True) -> None:
        item_number = (
            len(self.browser.find_elements_by_css_selector("#id_list_table tr")) + 1
        )
        self.get_input_box().send_keys(input_text)
        self.get_input_box().send_keys(Keys.ENTER)
        if validate:
            self.wait_for_row_in_list_table(f"{item_number}: {input_text}")

    def get_input_box(self):
        return self.browser.find_element_by_id("id_text")

    @staticmethod
    @wait
    def wait_for(fn):
        return fn()

    @wait
    def wait_to_be_logged_in(self, email: str):
        self.browser.find_element_by_link_text("Log out")
        self.assertIn(email, self.browser.find_element_by_css_selector(".navbar").text)

    @wait
    def wait_to_be_logged_out(self, email: str):
        self.browser.find_element_by_name("email")
        self.assertNotIn(
            email, self.browser.find_element_by_css_selector(".navbar").text
        )

    def create_pre_authenticated_session(self, email: str):
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
