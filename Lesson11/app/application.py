from selenium import webdriver

from pages.main_page import MainPage
from pages.prod_page import ProductPage
from pages.cart_page import CartPage


class Application:
    ''' класс для приложения litecart'''

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.main_page = MainPage(self.driver)
        self.prod_page = ProductPage(self.driver)
        self.cart_page = CartPage(self.driver)

    def quit(self):
        self.driver.quit()

    def save_screenshot(self, filename) -> bool:
        return self.driver.save_screenshot(filename)

    def add_prod_to_cart(self, n: int = 1):
        ''' Добавляем товар в корзину n-раз первый случайный товар с главной страницы'''

        for _ in range(n):
            self.main_page.open()
            self.main_page.first_product.click()

            self.prod_page.wait_to_open()
            self.prod_page.fill_all_required_fields()
            self.prod_page.click_add_cart_product()

    def delete_prod_from_cart(self, n: int = 0):
        '''  Открываем корзину и удаляем n первых товаров из корзины или все(если n<=0, или n > чем товаров в корзине)'''

        self.cart_page.open()
        max_n = self.cart_page.total_prod_in_cart()
        n = max_n if n <= 0 else min(max_n, n)
        for _ in range(n):
            self.cart_page.remove_cart_button.click()
            self.cart_page.wait_update_table()

    def check_quantity_in_cart(self, expected: int = 0) -> bool:
        ''' Сравниваем кол-во товаров в корзине с ожидаемым. '''

        self.main_page.open()
        return int(self.main_page.cart_preview.quantity) == expected


if __name__ == "__main__":
    pass