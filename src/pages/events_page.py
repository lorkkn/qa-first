import os
from src.pages.base_page import BasePage
from src.components.filter_panel import FilterPanel
from src.components.event_card import EventCard
from selenium.webdriver.support.ui import WebDriverWait
import allure
from dotenv import load_dotenv

load_dotenv()

class EventsPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.filter_panel = FilterPanel(driver)
        self.event_card = EventCard(driver)
        
        # Отримуємо URL з .env
        self.url = os.getenv("BASE_URL")

    @allure.step("Відкриття сторінки Events")
    def open_page(self):
        # Використовуємо URL, який дістали з .env
        self.open(self.url)

    @allure.step("Скролінг сторінки вниз для підрахунку загальної кількості подій")
    def scroll_and_get_total_count(self):
        current_count = len(self.find_elements(*self.event_card.CARD_ITEM))
        
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                WebDriverWait(self.driver, 3).until(
                    lambda d: len(self.find_elements(*self.event_card.CARD_ITEM)) > current_count
                )
                current_count = len(self.find_elements(*self.event_card.CARD_ITEM))
            except:
                self.driver.execute_script("window.scrollTo(0, 0);")
                break
                
        return current_count