from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By


class CartPreview:
    ''' Элемент с количеством товаров к корзине на главной и странице товара'''

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.quantity_locator = (By.CSS_SELECTOR, 'div#cart span.quantity')

    @property
    def quantity(self) -> str:
        return self.driver.find_element(*self.quantity_locator).text


if __name__ == "__main__":
    pass