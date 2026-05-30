# Лабораторна робота №1. Тестування на основі ризику
# Студент: Цар Володимир, група КН-32сп
# Варіант: SauceDemo (https://www.saucedemo.com/)

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Фікстура для запуску та закриття браузера перед/після кожного тесту
@pytest.fixture
def browser():
    # Запускаємо Chrome. На Mac можна також використати webdriver.Safari()
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

# -----------------------------------------------------------
# КРИТИЧНИЙ РИЗИК (High Priority)
# Якщо це не працює - бізнес зупиняється. Тестуємо першочергово.
# -----------------------------------------------------------
@pytest.mark.critical_risk
def test_login_successful(browser):
    """Перевірка успішної авторизації (Критичний ризик)"""
    browser.get("https://www.saucedemo.com/")
    
    # Знаходимо поля та вводимо дані
    browser.find_element(By.ID, "user-name").send_keys("standard_user")
    browser.find_element(By.ID, "password").send_keys("secret_sauce")
    browser.find_element(By.ID, "login-button").click()
    
    # Перевіряємо, що ми потрапили на сторінку товарів
    assert "inventory.html" in browser.current_url, "Помилка авторизації!"

# -----------------------------------------------------------
# СЕРЕДНІЙ РИЗИК (Medium Priority)
# Неприємно для користувача, але загалом сайт працює.
# -----------------------------------------------------------
@pytest.mark.medium_risk
def test_sorting_items(browser):
    """Перевірка сортування товарів (Середній ризик)"""
    # Спочатку треба залогінитись
    browser.get("https://www.saucedemo.com/")
    browser.find_element(By.ID, "user-name").send_keys("standard_user")
    browser.find_element(By.ID, "password").send_keys("secret_sauce")
    browser.find_element(By.ID, "login-button").click()
    
    # Клікаємо на сортування (наприклад, від Z до A)
    sort_dropdown = browser.find_element(By.CLASS_NAME, "product_sort_container")
    sort_dropdown.click()
    browser.find_element(By.XPATH, "//option[@value='za']").click()
    
    # Перевіряємо, чи змінилась активна опція
    active_option = browser.find_element(By.CLASS_NAME, "active_option").text
    assert active_option == "Name (Z to A)", "Сортування не спрацювало"

# -----------------------------------------------------------
# НИЗЬКИЙ РИЗИК (Low Priority)
# Незначні елементи, не впливають на продажі.
# -----------------------------------------------------------
@pytest.mark.low_risk
def test_twitter_link_presence(browser):
    """Перевірка наявності посилання на Twitter у футері (Низький ризик)"""
    browser.get("https://www.saucedemo.com/")
    browser.find_element(By.ID, "user-name").send_keys("standard_user")
    browser.find_element(By.ID, "password").send_keys("secret_sauce")
    browser.find_element(By.ID, "login-button").click()
    
    # Скролимо вниз і шукаємо лінк
    twitter_link = browser.find_element(By.CSS_SELECTOR, ".social_twitter a")
    assert twitter_link.is_displayed(), "Посилання на Twitter відсутнє"