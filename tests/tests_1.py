import unittest
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def wait_for_visible(self, locator, error_msg, timeout=5):
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
        except TimeoutException:
            raise AssertionError(error_msg) from None

    def click(self, locator, error_msg, timeout=5):
        element = self.wait_for_visible(locator, error_msg, timeout)
        element.click()

    def type_text(self, locator, text, error_msg, timeout=5):
        element = self.wait_for_visible(locator, error_msg, timeout)
        element.send_keys(text)

    def get_text(self, locator, error_msg, timeout=5):
        element = self.wait_for_visible(locator, error_msg, timeout)
        return element.text

    def is_displayed(self, locator, error_msg, timeout=5):
        element = self.wait_for_visible(locator, error_msg, timeout)
        return element.is_displayed()


class EventsPage(BasePage):
    URL = "https://www.greencity.cx.ua/#/greenCity/events"

    SEARCH_BUTTON = (By.CSS_SELECTOR, ".container-img.ng-star-inserted")
    SEARCH_BAR = (By.CSS_SELECTOR, "input[placeholder='Search']")
    FIRST_CARD_TITLE = (By.XPATH, "(//app-events-list-item)[1]//div[@class='event-title']/p")
    NOT_FOUND_MSG = (By.XPATH, "//app-events-list//p[@class='end-page-txt ng-star-inserted']")
    EVENT_CARD = (By.TAG_NAME, "app-events-list-item")
    
    DATE_DROPDOWN = (By.XPATH, "(//*[contains(@class, 'mat-mdc-select-arrow-wrapper')])[5]")
    CALENDAR_POPUP = (By.TAG_NAME, "mat-datepicker-content")
    START_DAY = (By.XPATH, "//*[contains(@class, 'mat-calendar-body-cell-content') and normalize-space(text())='1']")
    END_DAY = (By.XPATH, "//*[contains(@class, 'mat-calendar-body-cell-content') and normalize-space(text())='30']")
    FIRST_EVENT_DATE = (By.XPATH, "(//div[@class='date'])[1]")
    FILTER_CROSS = (By.XPATH, "//div[@class='cross-container']")

    def open(self):
        self.driver.get(self.URL)

    def open_search(self):
        self.click(self.SEARCH_BUTTON, "Search button is not clickable for 5 seconds")

    def search_for(self, text):
        self.type_text(self.SEARCH_BAR, text, "Search bar is not visible for 5 seconds")

    def get_first_event_title(self):
        return self.get_text(self.FIRST_CARD_TITLE, "First event card is not visible on the page")

    def is_not_found_msg_displayed(self):
        return self.is_displayed(self.NOT_FOUND_MSG, "No 'not found' message appeared for 5 seconds")

    def scroll_and_get_total_count(self):
        """Скролить сторінку до кінця і повертає загальну кількість подій."""
        elements = self.driver.find_elements(*self.EVENT_CARD)
        current_count = len(elements)
        
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(2) 
            elements = self.driver.find_elements(*self.EVENT_CARD)
            new_count = len(elements)
            
            if new_count == current_count:
                self.driver.execute_script("window.scrollTo(0, 0);")
                break
                
            current_count = new_count
        return current_count

    def select_date_range(self):
        self.click(self.DATE_DROPDOWN, "Date button is not clickable on the page")
        self.wait_for_visible(self.CALENDAR_POPUP, "Calendar popup did not appear")
        self.click(self.START_DAY, "Start date (1) is not clickable in the calendar")
        self.click(self.END_DAY, "End date (30) is not clickable in the calendar")

    def get_first_event_date(self):
        return self.get_text(self.FIRST_EVENT_DATE, "There are no events in this range")

    def clear_filters(self):
        self.click(self.FILTER_CROSS, "Filter not found in filter bar")
        sleep(2)


class TestEvents(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(1)
        self.driver.maximize_window()
        self.events_page = EventsPage(self.driver)
        self.events_page.open()

    def tearDown(self):
        if self.driver:
            self.driver.quit()

    def test_search_positive(self):
        self.events_page.open_search()
        
        first_card_text = self.events_page.get_first_event_title()
        self.events_page.search_for(first_card_text)
        
        new_first_card_text = self.events_page.get_first_event_title()
        self.assertEqual(first_card_text, new_first_card_text, "Searched event is not the first place in search")

    def test_search_negative(self):
        self.events_page.open_search()
        self.events_page.search_for("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        
        is_displayed = self.events_page.is_not_found_msg_displayed()
        self.assertTrue(is_displayed, "Not found message is not displayed")

    def test_date_picker(self):
        total_events = self.events_page.scroll_and_get_total_count()
        self.assertTrue(total_events > 0, "No events on the page")

        self.events_page.select_date_range()
        
        text_mon = self.events_page.get_first_event_date()
        is_april_en = "Apr" in text_mon and "2026" in text_mon
        is_april_uk = "квіт" in text_mon and "2026" in text_mon
        self.assertTrue(is_april_en or is_april_uk, f"Date error in first event: actual date was '{text_mon}'")

        self.events_page.clear_filters()
        total_events_new = self.events_page.scroll_and_get_total_count()
        self.assertEqual(total_events, total_events_new, "Total events number changed after using date filter")


if __name__ == "__main__":
    unittest.main()
