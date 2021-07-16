import re
import time

import poplib
import os

from django.core import mail
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from accounts.views import EMAIL_SUBJECT
from functional_tests.base import FunctionalTest


class SharingTest(FunctionalTest):
    @staticmethod
    def _quit_if_possible(browser):
        # noinspection PyBroadException
        try:
            browser.quit()
        except Exception:
            pass
        
    def test_can_get_email_link_to_log_in(self):
        # Jojo is pre-authenticated
        self.create_pre_authenticated_session("jojo@site.com")
        jojo_browser = self.browser
        self.addCleanup(lambda: self._quit_if_possible(jojo_browser))
        
        # Jojo's friend Maximilian is also hanging out on the lists site
        maximilian_browser = webdriver.Firefox()
        self.addCleanup(lambda: self._quit_if_possible(maximilian_browser))
        self.browser = maximilian_browser
        self.create_pre_authenticated_session("maximilian@site.net")
        
        # Jojo starts a list
        self.browser = jojo_browser
        self.browser.get(self.live_server_url)
        self.add_list_item("Get help")
        
        # Jojo notices a "Share this list" option
        share_box = self.browser.find_element_by_css_selector('input[name="sharee"]')
        self.assertEqual(share_box.get_attribute("placeholder"), "your-friend@example.com")
        


