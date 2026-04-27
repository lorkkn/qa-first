import os
import pytest
from selenium import webdriver
from dotenv import load_dotenv

# Завантажуємо змінні з .env файлу
load_dotenv(override=True)

@pytest.fixture(scope="function")
def driver():
    # Читаємо змінні (якщо їх немає в .env, беремо значення за замовчуванням)
    browser_name = os.getenv("BROWSER", "chrome").lower()
    is_headless = os.getenv("HEADLESS", "False").lower() == "true"

    if browser_name == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        
        # Застосовуємо headless режим, якщо в .env написано True
        if is_headless:
            options.add_argument("--headless")
            
        driver = webdriver.Chrome(options=options)
        driver.maximize_window()
    else:
        raise ValueError(f"Браузер {browser_name} не підтримується в цьому конфігу")

    yield driver
    driver.quit()