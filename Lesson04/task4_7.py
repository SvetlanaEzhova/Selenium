''' Сделайте сценарий, проверяющий наличие стикеров у всех товаров в учебном 
приложении litecart на главной странице. Стикеры - это полоски в левом верхнем 
углу изображения товара, на которых написано New или Sale или что-нибудь другое. 
Сценарий должен проверять, что у каждого товара имеется ровно один стикер. '''

from selenium import webdriver
from selenium.webdriver.common.by import By

if __name__ == "__main__":
    driver = webdriver.Chrome()
    result = True
    try:
        driver.get(url="http://localhost/litecart/")
        # получаем список всех li для товаров из трех разных разделов
        items = driver.find_elements(
            By.CSS_SELECTOR, 'div#main > div.middle > div.content > div.box li'
        )
        print('Всего карточек товара:', len(items))
        for item in items:
            # список стикеров внутри конкретного li
            stickers = item.find_elements(By.CSS_SELECTOR, 'div[class^=sticker]')
            if len(stickers) != 1:
                result = False
                break

    except Exception as ex:
        result = False
        print(f"Exception: {type(ex).__name__}")
        print(ex)
    finally:
        print('\nРезультат теста:', 'Пройден успешно' if result else '!!! Ошибка !!!', '\n')
        driver.quit()
