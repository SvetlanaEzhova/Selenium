from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By

from elements.cart_preview import CartPreview


class MainPage:
    ''' Главная страница litecart'''

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.cart_preview = CartPreview(self.driver)

    def open(self):
        self.driver.get(url="http://localhost/litecart/")
        return self

    @property
    def first_product(self) -> WebElement:
        return self.driver.find_element(By.CSS_SELECTOR, 'div#main a.link:first-child')


if __name__ == "__main__":
    pass
