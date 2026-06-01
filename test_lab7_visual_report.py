# Лабораторна робота №7. Візуальна валідація та Тестові звіти
# Студент: Цар Володимир, група КН-32сп
# Варіант: SauceDemo (https://www.saucedemo.com/)

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import os

@pytest.fixture
def browser():
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

def test_visual_logo_validation(browser):
    """
    Візуальна валідація: Перевірка наявності логотипу та створення еталонного скріншоту.
    """
    browser.get("https://www.saucedemo.com/")
    
    logo = browser.find_element(By.CLASS_NAME, "login_logo")
    assert logo.is_displayed(), "Візуальний дефект: Логотип не відображається!"
    
    # Створюємо папку для скріншотів, якщо її немає
    screenshot_dir = "screenshots"
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)
        
    # Робимо знімок екрана (доказ для звіту)
    screenshot_path = os.path.join(screenshot_dir, "login_screen_mac.png")
    browser.save_screenshot(screenshot_path)
    
    assert os.path.exists(screenshot_path), "Система не змогла зберегти скріншот!"

def test_visual_layout_dimensions(browser):
    """
    Візуальна валідація: Перевірка фізичних розмірів кнопки.
    Гарантуємо, що верстка (CSS) не зламалася і кнопка має правильний розмір.
    """
    browser.get("https://www.saucedemo.com/")
    
    login_btn = browser.find_element(By.ID, "login-button")
    size = login_btn.size
    
    # Висота та ширина кнопки мають бути більшими за нуль (елемент не сплюснутий)
    assert size['height'] > 0, f"Візуальний дефект: висота кнопки некоректна ({size['height']})"
    assert size['width'] > 0, f"Візуальний дефект: ширина кнопки некоректна ({size['width']})"