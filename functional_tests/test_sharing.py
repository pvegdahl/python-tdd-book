import re
import time

import poplib
import os

from django.core import mail
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from accounts.views import EMAIL_SUBJECT
from functional_tests.base import FunctionalTest
from functional_tests.list_page import ListPage


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
        jojo_email = "jojo@site.com"
        self.create_pre_authenticated_session(jojo_email)
        jojo_browser = self.browser
        self.addCleanup(lambda: self._quit_if_possible(jojo_browser))

        # Jojo's friend Maximilian is also hanging out on the lists site
        maximilian_browser = webdriver.Firefox()
        self.addCleanup(lambda: self._quit_if_possible(maximilian_browser))
        self.browser = maximilian_browser
        maximilian_email = "maximilian@site.net"
        self.create_pre_authenticated_session(maximilian_email)

        # Jojo starts a list
        self.browser = jojo_browser
        self.browser.get(self.live_server_url)
        list_item_text = "Get help"
        list_page = ListPage(self).add_list_item(list_item_text)

        # Jojo notices a "Share this list" option
        share_box = list_page.get_share_box()
        self.assertEqual(
            share_box.get_attribute("placeholder"), "your.friend@example.com"
        )

        # Jojo shares the list and the page updates to say it is shared with Maximilian
        list_page.share_list_with(maximilian_email)

        # Max now goes to the my lists page on his browser
        self.browser = maximilian_browser
        MyListsPage(self).go_to_my_lists_page()

        # Max sees Jojo's list in there!
        self.browser.find_element_by_link_text(list_item_text).click()

        # On the list page, Max sees that it is Jojo's list
        self.wait_for(lambda: self.assertEqual(list_page.get_list_owner(), jojo_email))

        # Max adds an item to the list
        max_item_text = "Hi Jojo!"
        list_page.add_list_item(max_item_text)

        # When Jojo refreshes the page, he sees the new item
        self.browser = jojo_browser
        self.browser.refresh()
        list_page.wait_for_row_in_list_table(item_text=max_item_text, item_number=2)
