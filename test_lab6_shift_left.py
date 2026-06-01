# Лабораторна робота №6. Тестування зі зсувом вліво (Shift-Left) та API
# Студент: Цар Володимир, група КН-32сп
# Варіант: SauceDemo (https://www.saucedemo.com/)

import pytest
import requests

# -----------------------------------------------------------
# 1. Модульне тестування (Unit Testing) - База піраміди тестування
# -----------------------------------------------------------
# Уявімо, що це наша власна функція для валідації та форматування логіну
# перед тим, як відправити його на сервер. Тестуємо її ізольовано.
def format_username(raw_username):
    """Видаляє зайві пробіли та переводить у нижній регістр"""
    if not isinstance(raw_username, str):
        raise ValueError("Логін має бути строкою")
    return raw_username.strip().lower()

def test_unit_format_username_valid():
    """Unit-тест: перевірка правильного форматування логіну"""
    assert format_username("  Standard_User  ") == "standard_user"

def test_unit_format_username_empty():
    """Unit-тест: перевірка поведінки з пустою строкою"""
    assert format_username("   ") == ""

def test_unit_format_username_invalid_type():
    """Unit-тест: перевірка обробки некоректних типів даних"""
    with pytest.raises(ValueError):
        format_username(12345)

# -----------------------------------------------------------
# 2. Інтеграційне / API Тестування - Середина піраміди
# -----------------------------------------------------------
# Shift-Left підхід: перевіряємо доступність ресурсу через API (швидко), 
# щоб не запускати дорогі UI-тести через Selenium, якщо сервер лежить.
def test_api_server_is_alive():
    """API-тест: Перевірка доступності головної сторінки SauceDemo"""
    url = "https://www.saucedemo.com/"
    
    # Робимо швидкий HTTP-запит без відкриття браузера
    response = requests.get(url, timeout=5)
    
    # Сервер має повернути статус 200 (OK)
    assert response.status_code == 200, f"Сервер недоступний! Статус код: {response.status_code}"
    
    # Перевіряємо, що сервер віддав потрібний контент (HTML сторінку)
    assert "text/html" in response.headers.get("Content-Type", ""), "Отримано невірний тип контенту"