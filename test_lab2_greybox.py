# Лабораторна робота №2. Сіре тестування (Grey-box testing)
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

def test_session_cookie_created_on_login(browser):
    """
    Сіре тестування: Перевіряємо не просто UI, а те, що система 
    створила правильну сесійну куку після логіну.
    """
    browser.get("https://www.saucedemo.com/")
    
    # Авторизація
    browser.find_element(By.ID, "user-name").send_keys("standard_user")
    browser.find_element(By.ID, "password").send_keys("secret_sauce")
    browser.find_element(By.ID, "login-button").click()
    
    # Заглядаємо "під капот" (White/Grey-box елемент)
    session_cookie = browser.get_cookie("session-username")
    
    # Перевіряємо, що кука існує і містить правильне значення
    assert session_cookie is not None, "Кука сесії не була створена!"
    assert session_cookie["value"] == "standard_user", "Неправильне значення сесії в куках"

def test_cart_state_in_local_storage(browser):
    """
    Сіре тестування: Додаємо товар і перевіряємо Local Storage браузера 
    через виконання JavaScript коду (комбінація UI та внутрішнього стану).
    """
    browser.get("https://www.saucedemo.com/")
    browser.find_element(By.ID, "user-name").send_keys("standard_user")
    browser.find_element(By.ID, "password").send_keys("secret_sauce")
    browser.find_element(By.ID, "login-button").click()
    
    # Додаємо перший товар у кошик через UI (Black-box)
    browser.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
    
    # Перевіряємо стан кошика у пам'яті браузера через JS (White-box)
    cart_contents = browser.execute_script("return window.localStorage.getItem('cart-contents');")
    
    # Значення в Local Storage зберігається у вигляді масиву з ID товару
    assert cart_contents is not None, "Локальне сховище кошика порожнє"
    assert "[4]" in cart_contents, f"Товар з ID 4 не зберігся у Local Storage. Фактичний вміст: {cart_contents}"