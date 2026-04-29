import allure
from src.pages.events_page import EventsPage

@allure.feature("Events Page")
@allure.story("Search Functionality")
class TestSearchPositive:
    
    @allure.title("Позитивний тест пошуку: знаходження існуючої події")
    def test_search_positive(self, driver):
        page = EventsPage(driver)
        page.open_page()
        
        # Отримуємо назву першої події для пошуку
        target_title = page.event_card.get_first_card_title()
        
        # Виконуємо пошук
        page.filter_panel.search_for(target_title)
        
        # Перевіряємо, чи перша знайдена подія відповідає пошуковому запиту
        actual_title = page.event_card.get_first_card_title()
        assert target_title in actual_title, f"Очікували {target_title}, але отримали {actual_title}"