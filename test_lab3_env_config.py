# Лабораторна робота №3. Тестування середовища та конфігурації
# Студент: Цар Володимир, група КН-32сп
# Варіант: SauceDemo (https://www.saucedemo.com/)

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

@pytest.fixture
def browser():
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

def test_mobile_environment_ui(browser):
    """
    Тестування середовища: Симуляція мобільного пристрою.
    Перевіряємо, чи адаптується меню під вузький екран.
    """
    # Встановлюємо розмір екрану як у типового смартфона (наприклад, 390x844)
    browser.set_window_size(390, 844) 
    browser.get("https://www.saucedemo.com/")
    
    browser.find_element(By.ID, "user-name").send_keys("standard_user")
    browser.find_element(By.ID, "password").send_keys("secret_sauce")
    browser.find_element(By.ID, "login-button").click()
    
    # На мобільному екрані кнопка меню має бути видимою у вигляді 'бургера'
    burger_menu = browser.find_element(By.ID, "react-burger-menu-btn")
    assert burger_menu.is_displayed(), "Помилка середовища: Бургер-меню не з'явилося на мобільному розширенні!"

def test_desktop_environment_ui(browser):
    """
    Тестування середовища: Симуляція десктопного монітора Full HD.
    """
    # Встановлюємо стандартний десктопний розмір
    browser.set_window_size(1920, 1080)
    browser.get("https://www.saucedemo.com/")
    
    # Перевіряємо, що логотип відображається коректно і не "з'їхав"
    login_logo = browser.find_element(By.CLASS_NAME, "login_logo")
    assert login_logo.is_displayed(), "Помилка середовища: Логотип не відображається на десктопі"

def test_locked_user_configuration(browser):
    """
    Тестування конфігурації: Перевірка роботи системи із заблокованим обліковим записом.
    """
    browser.get("https://www.saucedemo.com/")
    
    # Використовуємо іншу конфігурацію користувача (заблокований клієнт)
    browser.find_element(By.ID, "user-name").send_keys("locked_out_user")
    browser.find_element(By.ID, "password").send_keys("secret_sauce")
    browser.find_element(By.ID, "login-button").click()
    
    # Перевіряємо, чи система видає правильну помилку замість пускати на сайт
    error_msg = browser.find_element(By.CSS_SELECTOR, "[data-test='error']").text
    assert "locked out" in error_msg, "Система пропустила заблокованого користувача або видала невірну помилку!"