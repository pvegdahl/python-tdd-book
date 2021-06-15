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

    def _wait_for_row_in_list_table(self, row_text: str, timeout: int = 5) -> None:
        self._wait_for(
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

    def _send_input(self, input_text: str) -> None:
        input_box = self.browser.find_element_by_id("id_new_item")
        input_box.send_keys(input_text)
        input_box.send_keys(Keys.ENTER)

    @staticmethod
    def _wait_for(fn, timeout: int = 5):
        start_time = time.time()
        while True:
            try:
                return fn()
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > timeout:
                    raise e
                time.sleep(0.1)
