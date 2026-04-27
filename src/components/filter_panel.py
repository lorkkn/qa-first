from src.components.base_component import BaseComponent
from selenium.webdriver.common.by import By
import allure

class FilterPanel(BaseComponent):
    SEARCH_BUTTON = (By.CSS_SELECTOR, ".container-img.ng-star-inserted")
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[placeholder='Search']")
    NOT_FOUND_MSG = (By.XPATH, "//app-events-list//p[@class='end-page-txt ng-star-inserted']")
    
    DATE_FILTER_BTN = (By.XPATH, "(//*[contains(@class, 'mat-mdc-select-arrow-wrapper')])[5]")
    CALENDAR_POPUP = (By.TAG_NAME, "mat-datepicker-content")
    START_DAY = (By.XPATH, "//*[contains(@class, 'mat-calendar-body-cell-content') and normalize-space(text())='1']")
    END_DAY = (By.XPATH, "//*[contains(@class, 'mat-calendar-body-cell-content') and normalize-space(text())='30']")
    FILTER_CROSS = (By.XPATH, "//div[@class='cross-container']")

    @allure.step("Пошук події за текстом: {text}")
    def search_for(self, text):
        self.wait_for_visible(*self.SEARCH_BUTTON).click()
        search_bar = self.wait_for_visible(*self.SEARCH_INPUT)
        search_bar.clear()
        search_bar.send_keys(text)

    @allure.step("Перевірка відображення повідомлення 'Не знайдено'")
    def is_not_found_message_displayed(self):
        return self.wait_for_visible(*self.NOT_FOUND_MSG).is_displayed()

    @allure.step("Вибір діапазону дат (з 1 по 30 число)")
    def select_date_range(self):
        self.wait_for_visible(*self.DATE_FILTER_BTN).click()
        self.wait_for_visible(*self.CALENDAR_POPUP)
        self.wait_for_visible(*self.START_DAY).click()
        self.wait_for_visible(*self.END_DAY).click()

    @allure.step("Скидання фільтрів (натискання на хрестик)")
    def clear_filters(self):
        self.wait_for_visible(*self.FILTER_CROSS).click()