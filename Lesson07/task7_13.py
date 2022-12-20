''' Сделайте сценарий для добавления товаров в корзину и удаления товаров из корзины.

1) открыть главную страницу
2) открыть первый товар из списка
2) добавить его в корзину (при этом может случайно добавиться товар, который там уже есть, ничего страшного)
3) подождать, пока счётчик товаров в корзине обновится
4) вернуться на главную страницу, повторить предыдущие шаги ещё два раза, чтобы в общей сложности в корзине было 3 единицы товара
5) открыть корзину (в правом верхнем углу кликнуть по ссылке Checkout)
6) удалить все товары из корзины один за другим, после каждого удаления подождать, пока внизу обновится таблица '''

from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys


class driver_litecart(webdriver.Chrome):
    ''' класс с create\logout\login'''

    def add_prod_to_cart(self, n: int = 1):
        ''' Добавляем товар в корзину n-раз  первый случайный товар с главной страницы'''

        for _ in range(n):
            self.get(url="http://localhost/litecart/")
            total = self.find_element(By.CSS_SELECTOR, 'div#cart span.quantity').text

            self.find_element(By.CSS_SELECTOR, 'div#main a.link:first-child').click()
            WebDriverWait(driver=self, timeout=5).until(
                EC.element_to_be_clickable((By.NAME, 'add_cart_product'))
            )

            # если попался товар, у которого надо ввести размер (в тестовой базе - желтый товар)
            items = (self.find_elements(By.NAME, 'options[Size]'))
            if len(items) > 0:
                items[0].find_element(By.CSS_SELECTOR, 'option:last-child').click()

            self.find_element(By.NAME, 'add_cart_product').click()
            # WebDriverWait(driver=self, timeout=5).until(
            #     lambda x: x.find_element(By.CSS_SELECTOR, 'div#cart span.quantity').text != total
            # )
            WebDriverWait(driver=self, timeout=15).until_not(
                EC.text_to_be_present_in_element(
                    (By.CSS_SELECTOR, 'div#cart span.quantity'), total
                )
            )

    def open_cart(self):
        ''' Открываем корзину '''

        self.find_element(By.CSS_SELECTOR, 'div#cart> a.link').click()
        WebDriverWait(driver=self, timeout=5).until(
            EC.visibility_of_element_located((By.ID, 'box-checkout-summary'))
        )

    def delete_prod_from_cart(self, n: int = 0):
        '''  Удаляем n первых товаров из корзины или все, если n<=0, или n > чем товаров в корзине'''

        max_n = len(self.find_elements(By.CSS_SELECTOR, 'li.item'))
        n = max_n if n <= 0 else min(max_n, n)
        for _ in range(n):
            self.find_element(By.CSS_SELECTOR,
                              'li.item:first-child button[name=remove_cart_item]').click()
            item = self.find_element(By.ID, 'box-checkout-summary')
            WebDriverWait(driver=self, timeout=5).until(EC.staleness_of(item))


if __name__ == "__main__":

    driver = driver_litecart()
    result = True
    try:
        driver.add_prod_to_cart(3)
        driver.open_cart()
        driver.delete_prod_from_cart()

    except Exception as ex:
        result = False
        print(f"Exception: {type(ex).__name__}")
        print(ex)
        # если упали, то делаем скриншот, сохраняется в текущей папке
        driver.save_screenshot('scr_' + datetime.now().strftime('%Y%m%d%H%M%S') + '.png')

    finally:
        print('\nРезультат теста:', 'Пройден успешно' if result else '!!! Ошибка !!!', '\n')
        driver.quit()
