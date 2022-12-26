from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class CartPage:
    ''' Страница корзины'''

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver

    def open(self):
        self.driver.get(url='http://localhost/litecart/en/checkout')
        return self

    def total_prod_in_cart(self) -> int:
        return len(self.driver.find_elements(By.CSS_SELECTOR, 'li.item'))

    @property
    def remove_cart_button(self) -> WebElement:
        return self.driver.find_element(
            By.CSS_SELECTOR, 'li.item:first-child button[name=remove_cart_item]'
        )

    def wait_update_table(self):
        WebDriverWait(driver=self.driver, timeout=5).until(
            EC.staleness_of(self.driver.find_element(By.ID, 'box-checkout-summary'))
        )


if __name__ == "__main__":
    pass