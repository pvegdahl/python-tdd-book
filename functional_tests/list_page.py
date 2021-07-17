from selenium.webdriver.common.keys import Keys
from typing import List

from selenium.webdriver.remote.webelement import WebElement

from functional_tests.base import FunctionalTest, wait


class ListPage:
    def __init__(self, test: FunctionalTest):
        self.test = test
        
    def get_table_rows(self) -> List[WebElement]:
        return self.test.browser.find_elements_by_css_selector("#id_list_table tr")
    
    @wait
    def wait_for_row_in_list_table(self, item_text: str, item_number: int) -> None:
        expected_row_text = f"{item_number}: {item_text}"
        rows = self.get_table_rows()
        self.test.assertIn(expected_row_text, [row.text for row in rows])
    
    def get_input_box(self) -> WebElement:
        return self.test.browser.find_element_by_id("id_text")

    def add_list_item(self, input_text: str, validate: bool = True) -> "ListPage":
        new_item_number = len(self.get_table_rows()) + 1
        self.get_input_box().send_keys(input_text)
        self.get_input_box().send_keys(Keys.ENTER)
        if validate:
            self.wait_for_row_in_list_table(item_text=input_text, item_number=new_item_number)
        return self
    
    def get_share_box(self) -> WebElement:
        return self.test.browser.find_element_by_css_selector('input[name="sharee"]')

    def get_shared_with_list(self) -> List[WebElement]:
        return self.test.browser.find_elements_by_css_selector(".list-sharee")
    
    def share_list_with(self, email: str) -> None:
        self.get_share_box().send_keys(email)
        self.get_share_box().send_keys(Keys.ENTER)
        self.test.wait_for(lambda: self.test.assertIn(email, [item.text for item in self.get_shared_with_list()]))

    def get_list_owner(self) -> str:
        return self.test.browser.find_element_by_id("id_list_owner").text
