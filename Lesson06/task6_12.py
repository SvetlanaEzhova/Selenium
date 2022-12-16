''' Сделайте сценарий для добавления нового товара (продукта) в учебном приложении litecart (в админке).
  Для добавления товара нужно открыть меню Catalog, в правом верхнем углу нажать кнопку "Add New Product", 
заполнить поля с информацией о товаре и сохранить.
  Достаточно заполнить только информацию на вкладках General, Information и Prices. Скидки (Campains) на 
вкладке Prices можно не добавлять.
  Переключение между вкладками происходит не мгновенно, поэтому после переключения можно сделать небольшую 
паузу (о том, как делать более правильные ожидания, будет рассказано в следующих занятиях).
  Картинку с изображением товара нужно уложить в репозиторий вместе с кодом. При этом указывать в коде полный 
абсолютный путь к файлу плохо, на другой машине работать не будет. Надо средствами языка программирования 
преобразовать относительный путь в абсолютный.
  После сохранения товара нужно убедиться, что он появился в каталоге (в админке). Клиентскую часть магазина 
можно не проверять. '''

from datetime import datetime

import sys, os

#from os import path

# sys.path.append(os.path.abspath('.'))

from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys


def click_checkbox(item: WebElement, on: bool = True):
    if on != item.get_property('checked'): item.click()


def clear_and_input(item: WebElement, val: str):
    item.clear()
    item.send_keys(val)


class driver_litecart(webdriver.Chrome):
    ''' класс с create\logout\login'''

    def login(self, user: str = 'admin', password: str = 'admin') -> None:
        ''' Логинится на указанный ресурс, если не смог, то упадет с TimeoutException '''

        self.find_element(By.NAME, 'username').send_keys(user)
        self.find_element(By.NAME, 'password').send_keys(password)
        self.find_element(By.NAME, 'login').click()
        WebDriverWait(driver=self,
                      timeout=10).until(EC.presence_of_element_located((By.ID, 'body-wrapper')))

    def click_add_new_product(self):
        '''  Кликаем на Catalog в столбце слева, ждем обновления содержимого страницы, 
        нажимаем Add New Product и ждем возможности водить данные'''

        self.find_element(By.ID, 'box-apps-menu').find_element(By.LINK_TEXT, 'Catalog').click()
        WebDriverWait(driver=self,
                      timeout=10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'dataTable')))
        self.find_element(By.ID, 'content').find_element(By.PARTIAL_LINK_TEXT,
                                                         'Add New Product').click()
        WebDriverWait(driver=self,
                      timeout=10).until(EC.element_to_be_clickable((By.LINK_TEXT, 'General')))

    def fill_general_tab(self, pname: str, pcode: str):
        ''' Заполняем необходимые поля на вкладке General (первые две строки, просто для унификации заполнения всех вкладок)'''

        self.find_element(By.LINK_TEXT, 'General').click()
        WebDriverWait(driver=self,
                      timeout=10).until(EC.element_to_be_clickable((By.NAME, 'date_valid_to')))
        self.find_element(By.CSS_SELECTOR, 'input[name=status][value="1"').click()
        self.find_element(By.NAME, 'name[en]').send_keys(pname)
        self.find_element(By.NAME, 'code').send_keys(pcode)
        click_checkbox(on=False, item=self.find_element(By.CSS_SELECTOR, 'input[data-name=Root]'))
        click_checkbox(
            on=True, item=self.find_element(By.CSS_SELECTOR, 'input[data-name="Rubber Ducks"]')
        )
        clear_and_input(self.find_element(By.NAME, 'quantity'), '30.00')
        self.find_element(By.CSS_SELECTOR,
                          'select[name=sold_out_status_id] > option[value="2"]').click()

        # картинка должна быть там же где и питоновский скрипт
        fpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Pict1.png')
        self.find_element(By.NAME, 'new_images[]').send_keys(fpath)

    def fill_information_tab(self):
        ''' Заполняем необходимые поля на вкладке Information '''

        self.find_element(By.LINK_TEXT, 'Information').click()
        WebDriverWait(driver=self,
                      timeout=10).until(EC.element_to_be_clickable((By.NAME, 'manufacturer_id')))
        self.find_element(By.CSS_SELECTOR,
                          'select[name=manufacturer_id] > option:last-child').click()
        self.find_element(By.NAME, 'short_description[en]').send_keys('Short text')
        self.find_element(By.CLASS_NAME, 'trumbowyg-editor').send_keys('Long long text')

    def fill_prices_tab(self):
        ''' Заполняем необходимые поля на вкладке Prices '''

        self.find_element(By.LINK_TEXT, 'Prices').click()
        WebDriverWait(driver=self, timeout=10).until(
            EC.visibility_of_element_located((By.NAME, 'purchase_price'))
        )
        clear_and_input(self.find_element(By.NAME, 'purchase_price'), '15.00')
        self.find_element(By.NAME, 'purchase_price_currency_code').send_keys('USD' + Keys.ENTER)
        self.find_element(By.NAME, 'prices[USD]').send_keys('20')

    def click_save(self):
        '''  Нажимаем Save и ждем когда вернемся к списку'''

        self.find_element(By.NAME, 'save').click()
        WebDriverWait(driver=self,
                      timeout=10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'dataTable')))


if __name__ == "__main__":
    driver = driver_litecart()

    result = True
    try:
        driver.get(url='http://localhost/litecart/admin/')
        driver.login()

        driver.click_add_new_product()

        # создадим достаточно уникальное имя товара, чтобы потом было просто проверять, что товар добавился
        uniq_st = datetime.now().strftime('%H%M%S')
        prod_name = 'Blue Duck with spot ' + uniq_st
        driver.fill_general_tab(pname=prod_name, pcode=uniq_st)
        driver.fill_information_tab()
        driver.fill_prices_tab()

        driver.click_save()

        result = result and len(driver.find_elements(By.LINK_TEXT, prod_name)) > 0
        print('Товар' if result else 'Товар НЕ', 'появился в каталоге (в админке)')

        driver.save_screenshot('scr2_' + datetime.now().strftime('%Y%m%d%H%M%S') + '.png')

    except Exception as ex:
        result = False
        print(f"Exception: {type(ex).__name__}")
        print(ex)
        # если упали, то делаем скриншот, сохраняется в текущей папке
        driver.save_screenshot('scr_' + datetime.now().strftime('%Y%m%d%H%M%S') + '.png')

    finally:
        print('\nРезультат теста:', 'Пройден успешно' if result else '!!! Ошибка !!!', '\n')
        driver.quit()
