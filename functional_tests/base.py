import os
import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys


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

    def wait_for_row_in_list_table(self, row_text: str, timeout: int = 5) -> None:
        self.wait_for(
            fn=lambda: self.assertIn(
                row_text,
                [
                    row.text
                    for row in (
                        self.browser.find_element_by_id(
                            "id_list_table"
                        ).find_elements_by_tag_name("tr")
                    )
                ],
            ),
            timeout=timeout,
        )

    def send_input(self, input_text: str) -> None:
        input_box = self.get_input_box()
        input_box.send_keys(input_text)
        input_box.send_keys(Keys.ENTER)

    def get_input_box(self):
        return self.browser.find_element_by_id("id_text")

    @staticmethod
    def wait_for(fn, timeout: int = 5):
        start_time = time.time()
        while True:
            try:
                return fn()
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > timeout:
                    raise e
                time.sleep(0.1)

    def wait_to_be_logged_in(self, email: str):
        self.wait_for(lambda: self.browser.find_element_by_link_text("Log out"))
        self.assertIn(email, self.browser.find_element_by_css_selector(".navbar").text)

    def wait_to_be_logged_out(self, email: str):
        self.wait_for(lambda: self.browser.find_element_by_name("email"))
        self.assertNotIn(
            email, self.browser.find_element_by_css_selector(".navbar").text
        )
