import allure
from src.pages.events_page import EventsPage

@allure.feature("Events Page")
@allure.story("Filter Functionality")
class TestDatePicker:
    
    @allure.title("Фільтрація подій за допомогою Date Picker")
    def test_date_picker(self, driver):
        page = EventsPage(driver)
        page.open_page()
        
        total_events_initial = page.scroll_and_get_total_count()
        assert total_events_initial > 0, "No events on the page"
        
        page.filter_panel.select_date_range()
        
        first_date_text = page.event_card.get_first_card_date()
        
        # Перевіряємо наявність дня та місяця
        is_april = any(month in first_date_text for month in ["Apr", "квіт"])
        assert is_april, f"Очікували подію у квітні, але отримали дату: {first_date_text}"
        
        page.filter_panel.clear_filters()
        
        # Іменована функція замість лямбди для перевірки відновлення результатів
        def count_is_restored(d):
            return page.scroll_and_get_total_count() == total_events_initial

        # Explicit wait після очищення фільтру
        page.wait.until(
            count_is_restored,
            message=f"Кількість подій не повернулася до {total_events_initial} після очищення фільтру"
        )