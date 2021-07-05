import os
import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys


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
        staging_server = os.environ.get("STAGING_SERVER")
        if staging_server:
            # noinspection HttpUrlsUsage
            self.live_server_url = f"http://{staging_server}"

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

    def send_input(self, input_text: str) -> None:
        input_box = self.get_input_box()
        input_box.send_keys(input_text)
        input_box.send_keys(Keys.ENTER)

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
