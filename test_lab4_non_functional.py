# Лабораторна робота №4. Нефункціональне тестування (Performance)
# Студент: Цар Володимир, група КН-32сп
# Варіант: SauceDemo (https://www.saucedemo.com/)

import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

@pytest.fixture
def browser():
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

def test_page_load_performance(browser):
    """
    Нефункціональне тестування (Продуктивність): 
    Перевіряємо, що сторінка товарів завантажується швидше ніж за 2 секунди.
    """
    # Логінимось
    browser.get("https://www.saucedemo.com/")
    browser.find_element(By.ID, "user-name").send_keys("standard_user")
    browser.find_element(By.ID, "password").send_keys("secret_sauce")
    
    # Фіксуємо час перед кліком
    start_time = time.time()
    
    browser.find_element(By.ID, "login-button").click()
    
    # Чекаємо, поки з'явиться контейнер з товарами
    inventory_container = browser.find_element(By.ID, "inventory_container")
    assert inventory_container.is_displayed()
    
    # Фіксуємо час після завантаження
    end_time = time.time()
    
    # Рахуємо тривалість
    load_time = end_time - start_time
    
    print(f"\nЧас завантаження каталогу: {load_time:.2f} секунд")
    
    # Нефункціональна вимога: час має бути < 2.0 секунд
    assert load_time < 2.0, f"Сторінка завантажується занадто довго: {load_time:.2f} сек"

def test_image_rendering_performance(browser):
    """
    Нефункціональне тестування (Відмальовка UI):
    Перевіряємо чи всі зображення товарів завантажились коректно (не биті лінки).
    """
    browser.get("https://www.saucedemo.com/")
    browser.find_element(By.ID, "user-name").send_keys("standard_user")
    browser.find_element(By.ID, "password").send_keys("secret_sauce")
    browser.find_element(By.ID, "login-button").click()
    
    # Знаходимо всі зображення товарів на сторінці
    images = browser.find_elements(By.CLASS_NAME, "inventory_item_img")
    
    for img in images:
        # За допомогою JavaScript перевіряємо, чи картинка фізично відрендерилась
        is_loaded = browser.execute_script(
            "return arguments[0].complete && typeof arguments[0].naturalWidth != 'undefined' && arguments[0].naturalWidth > 0", 
            img.find_element(By.TAG_NAME, "img")
        )
        assert is_loaded, "Виявлено зламане зображення товару! Помилка рендерингу (UI/UX)."