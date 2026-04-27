import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import allure
from dotenv import load_dotenv

load_dotenv()

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        # Отримуємо TIMEOUT з .env, перетворюємо в integer (число)
        timeout_env = int(os.getenv("TIMEOUT", 10))
        self.wait = WebDriverWait(self.driver, timeout_env)

    @allure.step("Відкриття URL: {url}")
    def open(self, url):
        self.driver.get(url)

    def wait_for_visible(self, by, locator, timeout=None):
        # Якщо специфічний таймаут не передано, беремо базовий з .env
        actual_timeout = timeout if timeout else int(os.getenv("TIMEOUT", 10))
        try:
            return WebDriverWait(self.driver, actual_timeout).until(
                EC.visibility_of_element_located((by, locator))
            )
        except TimeoutException:
            raise AssertionError(f"Елемент {locator} не знайдено протягом {actual_timeout} секунд")

    def find_elements(self, by, locator):
        return self.driver.find_elements(by, locator)