import pytest
import allure
from src.pages.events_page import EventsPage

@allure.feature("Events Page Functionality")
class TestEvents:

    @allure.story("Search Functionality")
    @allure.title("Позитивний тест пошуку: знаходження існуючої події")
    def test_search_positive(self, driver):
        page = EventsPage(driver)
        page.open_page()
        
        target_title = page.event_card.get_first_card_title()
        page.filter_panel.search_for(target_title)
        
        # Перевіряємо, що після пошуку перша картка відповідає запиту
        new_title = page.event_card.get_first_card_title()
        assert target_title == new_title, "Searched event is not the first place in search"

    @allure.story("Search Functionality")
    @allure.title("Негативний тест пошуку: неіснуюча подія")
    def test_search_negative(self, driver):
        page = EventsPage(driver)
        page.open_page()
        
        page.filter_panel.search_for("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        
        assert page.filter_panel.is_not_found_message_displayed(), "Not found message is not displayed"

    @allure.story("Filter Functionality")
    @allure.title("Фільтрація подій за допомогою Date Picker")
    def test_date_picker(self, driver):
        page = EventsPage(driver)
        page.open_page()
        
        # Отримуємо початкову кількість подій
        total_events_initial = page.scroll_and_get_total_count()
        assert total_events_initial > 0, "No events on the page"
        
        # Вибираємо діапазон у квітні
        page.filter_panel.select_date_range()
        
        # Отримуємо дату першої картки
        first_date_text = page.event_card.get_first_card_date()
        
        # Перевіряємо, чи дата містить "квітень" (UA) або "April" (EN) будь-якого числа
        # Це дозволить тесту проходити для 1, 15 чи 30 квітня
        is_april = any(month in first_date_text for month in ["Apr", "квіт"])
        assert is_april, f"Очікували подію у квітні, але отримали дату: {first_date_text}"
        
        # Очищуємо фільтри
        page.filter_panel.clear_filters()
        
        # Створюємо іменовану функцію замість лямбди для перевірки умови
        def count_is_restored(d):
            return page.scroll_and_get_total_count() == total_events_initial

        # Використовуємо функцію у WebDriverWait
        page.wait.until(
            count_is_restored,
            message=f"Кількість подій не повернулася до {total_events_initial} після очищення фільтру"
        )