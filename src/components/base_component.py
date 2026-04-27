from src.pages.base_page import BasePage

class BaseComponent(BasePage):
    """Базовий клас для всіх UI компонентів. Наслідує методи пошуку та очікувань з BasePage."""
    def __init__(self, driver):
        super().__init__(driver)