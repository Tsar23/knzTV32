# Лабораторна робота №5. Тестові оракули, евристика та техніки тест-дизайну
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

# Використовуємо динамічні техніки: "Таблиці прийняття рішень" та "Еквівалентне розділення".
# Параметризуємо один тест для перевірки 4 різних сценаріїв (класів).
@pytest.mark.parametrize("username, password, expected_oracle", [
    ("standard_user", "secret_sauce", "success_url"),      # Валідні дані (Позитивний тест)
    ("locked_out_user", "secret_sauce", "error_message"),  # Заблокований акаунт (Негативний)
    ("standard_user", "wrong_pass", "error_message"),      # Невірний пароль (Негативний)
    ("", "", "error_message")                              # Пусті поля (Граничне значення)
])
def test_login_decision_table_and_oracles(browser, username, password, expected_oracle):
    """
    Тестування за допомогою таблиць прийняття рішень (динамічний аналіз чорного ящика).
    Ми використовуємо різні Тестові Оракули залежно від очікуваного результату.
    """
    browser.get("https://www.saucedemo.com/")
    
    # Вводимо дані (якщо вони не пусті)
    if username:
        browser.find_element(By.ID, "user-name").send_keys(username)
    if password:
        browser.find_element(By.ID, "password").send_keys(password)
        
    browser.find_element(By.ID, "login-button").click()
    
    # -------------------------------------------------------------
    # ТЕСТОВІ ОРАКУЛИ (Механізми визначення результату тесту)
    # -------------------------------------------------------------
    
    if expected_oracle == "success_url":
        # Оракул 1: Перевірка зміни стану системи (URL)
        assert "inventory.html" in browser.current_url, "Оракул 'success_url' виявив помилку: вхід не виконано."
    
    elif expected_oracle == "error_message":
        # Оракул 2: Перевірка інтерфейсу на наявність повідомлення про помилку
        error_element = browser.find_element(By.CSS_SELECTOR, "[data-test='error']")
        assert error_element.is_displayed(), "Оракул 'error_message' виявив помилку: повідомлення відсутнє."
        
        # Евристика: перевіряємо, чи текст помилки логічно відповідає нашій дії
        error_text = error_element.text
        if username == "locked_out_user":
            assert "locked out" in error_text, "Евристика не збігається: невірний текст блокування."
        elif username == "" and password == "":
            assert "Username is required" in error_text, "Евристика не збігається: система не просить логін."
        else:
            assert "Username and password do not match" in error_text, "Евристика не збігається: помилка пари логін/пароль."