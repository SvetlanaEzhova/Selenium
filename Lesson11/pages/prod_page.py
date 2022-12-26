from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from elements.cart_preview import CartPreview


class ProductPage:
    ''' Страница товара'''

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.cart_preview = CartPreview(self.driver)

    @property
    def add_cart_product(self) -> WebElement:
        return self.driver.find_element(By.NAME, 'add_cart_product')

    def wait_to_open(self):
        WebDriverWait(driver=self.driver,
                      timeout=5).until(EC.element_to_be_clickable(self.add_cart_product))

    def click_add_cart_product(self):
        total = self.cart_preview.quantity
        self.add_cart_product.click()
        WebDriverWait(driver=self.driver, timeout=15).until_not(
            EC.text_to_be_present_in_element(self.cart_preview.quantity_locator, total)
        )

    def fill_all_required_fields(self):
        ''' если попался товар, у которого надо ввести размер (в тестовой базе - желтый товар) '''
        items = (self.driver.find_elements(By.NAME, 'options[Size]'))
        if len(items) > 0:
            items[0].find_element(By.CSS_SELECTOR, 'option:last-child').click()


if __name__ == "__main__":
    pass