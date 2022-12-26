''' Переделайте созданный в задании 13 сценарий для добавления товаров в корзину и удаления 
товаров из корзины, чтобы он использовал многослойную архитектуру.

А именно, выделите вспомогательные классы для работы с главной страницей (откуда выбирается товар), 
для работы со страницей товара (откуда происходит добавление товара в корзину), со страницей корзины 
(откуда происходит удаление), и реализуйте сценарий, который не напрямую обращается к операциям 
Selenium, а оперирует вышеперечисленными объектами-страницами. '''

from datetime import datetime
from app.application import Application

if __name__ == "__main__":

    app = Application()
    result = True
    try:
        app.add_prod_to_cart(3)
        app.delete_prod_from_cart()
        result = app.check_quantity_in_cart(0)

    except Exception as ex:
        result = False
        print(f"Exception: {type(ex).__name__}")
        print(ex)

    finally:
        print('\nРезультат теста:', 'Пройден успешно' if result else '!!! Ошибка !!!', '\n')
        if not result:
            app.save_screenshot('scr_' + datetime.now().strftime('%Y%m%d%H%M%S') + '.png')
        app.quit()
