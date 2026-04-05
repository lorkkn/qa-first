import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class TestEvents(unittest.TestCase):
    BASE_URL = "https://www.greencity.cx.ua/#/greenCity/events"
    def setUp(self):

        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(1)
        self.driver.maximize_window()
        self.driver.get(self.BASE_URL)

    def tearDown(self):
        if self.driver:
            self.driver.quit()


    def wait_for_visible(self, by, locator, error_msg, timeout=5):
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((by, locator))
            )
        except TimeoutException:
            raise AssertionError(error_msg) from None

        
    def scroll_and_get_total_count(self, by, locator):
        """
        Скролить сторінку до кінця і повертає загальну кількість елементів.
        """
        elements = self.driver.find_elements(by, locator)
        current_count = len(elements)
        
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
            sleep(2) 
            
            elements = self.driver.find_elements(by, locator)
            new_count = len(elements)
            
            if new_count == current_count:
                self.driver.execute_script("window.scrollTo(0, 0);")
                break
                
            current_count = new_count
            
        return current_count


    def test_search_positive(self):
        search_button = self.wait_for_visible(
            By.CSS_SELECTOR, ".container-img.ng-star-inserted", 
            "Search button is not clickable for 5 seconds"
        )
        search_button.click()
        
        search_bar = self.wait_for_visible(
            By.CSS_SELECTOR, "input[placeholder='Search']", 
            "Search bar is not visible for 5 seconds"
        )
        firstcard_selector = "(//app-events-list-item)[1]//div[@class='event-title']/p"
        firstcard = self.wait_for_visible(
            By.XPATH, firstcard_selector, 
            "First event card is not visible on the page"
        )
        firstcard_text = firstcard.text
        
        search_bar.send_keys(firstcard_text)
        
        new_firstcard = self.wait_for_visible(
            By.XPATH, firstcard_selector, 
            "No text cards for 5 seconds. Search doesn't work"
        )
            
        self.assertEqual(firstcard_text, new_firstcard.text, "Searched event is not the first place in search")
        

    def test_search_negative(self):
        search_button = self.wait_for_visible(
            By.CSS_SELECTOR, ".container-img.ng-star-inserted", 
            "Search button is not clickable for 5 seconds"
        )
        search_button.click()
        
        search_bar = self.wait_for_visible(
            By.CSS_SELECTOR, "input[placeholder='Search']", 
            "Search bar is not visible for 5 seconds"
        )
        search_bar.send_keys("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        
        errortext = self.wait_for_visible(
            By.XPATH, "//app-events-list//p[@class='end-page-txt ng-star-inserted']", 
            "No 'not found' message appeared for 5 seconds"
        )
        self.assertTrue(errortext.is_displayed(), "Not found message is not displayed")

    def test_date_picker(self):
        event_card_selector = "app-events-list-item" 
        total_events = self.scroll_and_get_total_count(By.TAG_NAME, event_card_selector)
        self.assertTrue(total_events > 0, "No events on the page")

        date_button_selector = "(//*[contains(@class, 'mat-mdc-select-arrow-wrapper')])[5]"
        date_button = self.wait_for_visible(
            By.XPATH, date_button_selector, 
            "Date button is not clickable on the page"
        )      
        date_button.click()
        
        calendar_popup_selector = "mat-datepicker-content"
        
        self.wait_for_visible(
            By.TAG_NAME, calendar_popup_selector,
            "Calendar popup did not appear after clicking the date input"
        )
        

        start_day_xpath = "//*[contains(@class, 'mat-calendar-body-cell-content') and normalize-space(text())='1']"
        
        start_day = self.wait_for_visible(
            By.XPATH, start_day_xpath, 
            "Start date (12) is not clickable in the calendar"
        )
        start_day.click()
        
        end_day_xpath = "//*[contains(@class, 'mat-calendar-body-cell-content') and normalize-space(text())='30']"
        
        end_day = self.wait_for_visible(
            By.XPATH, end_day_xpath, 
            "End date (30) is not clickable in the calendar"
        )
        end_day.click()

        first_date_selector = "//div[@class = \"date\"]"
        first_date = self.wait_for_visible(
            By.XPATH, first_date_selector, 
            "There are no events in this range"
        )
        first_date_bool = first_date.text == "Apr 1, 2026" or first_date.text == "1 квіт. 2026 р."
        self.assertTrue(first_date_bool,"Date error in first event")
        filter_cross_xpath = "//div[@class = \"cross-container\"]"
        filter_cross = self.wait_for_visible(
            By.XPATH, filter_cross_xpath, 
            "Filter not found in filter bar"
        )
        filter_cross.click()
        total_events_new = self.scroll_and_get_total_count(By.TAG_NAME, event_card_selector)
        self.assertEqual(total_events,total_events_new,"Total events number changed after using date filter")
        sleep(2)

if __name__ == "__main__":
    unittest.main()
