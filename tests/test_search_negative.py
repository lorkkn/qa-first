import allure
from src.pages.events_page import EventsPage

@allure.feature("Events Page")
@allure.story("Search Functionality")
class TestSearchNegative:
    
    @allure.title("Негативний тест пошуку: неіснуюча подія")
    def test_search_negative(self, driver):
        page = EventsPage(driver)
        page.open_page()
        
        invalid_search_query = "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
        
        # Виконуємо пошук за невалідними даними
        page.filter_panel.search_for(invalid_search_query)
        
        # Отримуємо загальну кількість подій після пошуку
        # Очікується, що карток не буде (0)
        current_count = len(page.find_elements(*page.event_card.CARD_ITEM))
        assert current_count == 0, f"Очікували 0 подій, але знайдено {current_count}"