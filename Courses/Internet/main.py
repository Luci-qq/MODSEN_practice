from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC

# ChromeDriver
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)

# 1. Работа с LocalStorage

# Открываем веб-страницу
driver.get("https://www.selenium.dev/")

# Устанавливаем значение в LocalStorage
driver.execute_script("localStorage.setItem('testKey', 'HelloModsen');")

# Получаем значение из LocalStorage
value = driver.execute_script("return localStorage.getItem('testKey');")
print(f"Значение из LocalStorage: {value}")

# Удаляем значение из LocalStorage
driver.execute_script("localStorage.removeItem('testKey');")

# Проверяем, что значение удалено
value = driver.execute_script("return localStorage.getItem('testKey');")
print(f"Значение после удаления: {value}")

# 2. Работа с Cookies

# Открываем веб-страницу
driver.get("https://www.selenium.dev/")

# Устанавливаем cookie
driver.add_cookie({"name": "ModsenCookie", "value": "CookieModsen"})

# Получаем значение cookie
cookie = driver.get_cookie("ModsenCookie")
print(f"Значение cookie: {cookie['value']}")

# Удаляем cookie
driver.delete_cookie("ModsenCookie")

# Проверяем, что cookie удалено
cookie = driver.get_cookie("ModsenCookie")
print(f"Cookie после удаления: {cookie}")

# Закрываем браузер
driver.quit()