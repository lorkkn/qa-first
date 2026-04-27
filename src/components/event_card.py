from src.components.base_component import BaseComponent
from selenium.webdriver.common.by import By
import allure

class EventCard(BaseComponent):
    CARD_ITEM = (By.TAG_NAME, "app-events-list-item")
    FIRST_CARD_TITLE = (By.XPATH, "(//app-events-list-item)[1]//div[@class='event-title']/p")
    FIRST_CARD_DATE = (By.XPATH, "//div[@class='date']")

    @allure.step("Отримання заголовка першої картки події")
    def get_first_card_title(self):
        return self.wait_for_visible(*self.FIRST_CARD_TITLE).text

    @allure.step("Отримання дати першої картки події")
    def get_first_card_date(self):
        return self.wait_for_visible(*self.FIRST_CARD_DATE).text