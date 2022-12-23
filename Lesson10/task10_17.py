''' Сделайте сценарий, который проверяет, не появляются ли в логе браузера сообщения при открытии страниц 
в учебном приложении, а именно -- страниц товаров в каталоге в административной панели.

Сценарий должен состоять из следующих частей:

1) зайти в админку
2) открыть каталог, категорию, которая содержит товары 
    (страница http://localhost/litecart/admin/?app=catalog&doc=catalog&category_id=1)
3) последовательно открывать страницы товаров и проверять, не появляются ли в логе браузера сообщения (любого уровня) '''

from datetime import datetime
from pprint import pprint

from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class driver_litecart(webdriver.Chrome):
    ''' класс с create\logout\login'''

    def login(self, user: str = 'admin', password: str = 'admin') -> None:
        ''' Логинится на указанный ресурс, если не смог, то упадет с TimeoutException '''

        self.find_element(By.NAME, 'username').send_keys(user)
        self.find_element(By.NAME, 'password').send_keys(password)
        self.find_element(By.NAME, 'login').click()
        WebDriverWait(driver=self,
                      timeout=10).until(EC.presence_of_element_located((By.ID, 'body-wrapper')))

    def click_on_catalog(self):
        ''' Кликаем на Catalog в столбце слева, ждем обновления содержимого страницы '''

        self.find_element(By.ID, 'box-apps-menu').find_element(By.LINK_TEXT, 'Catalog').click()
        WebDriverWait(driver=self,
                      timeout=10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'dataTable')))

    def open_all_closed_folders(self):
        ''' Открываем все закрытые папки справа (категории\подкатегории товара)'''

        while True:
            items = self.find_elements(
                By.XPATH, '//tr[@class="row"]/td[3]/i[@class="fa fa-folder"]/..//a'
            )
            if len(items) == 0: break
            items[0].click()

    def get_links_for_all_products(self) -> list:
        ''' Возвращаем список ссылок на страницы товаров '''

        return [
            item.get_attribute('href')
            for item in self.find_elements(By.XPATH, '//tr[@class="row"]/td[3]/img/..//a')
        ]


if __name__ == "__main__":

    caps = webdriver.DesiredCapabilities.CHROME.copy()
    # caps['goog:loggingPrefs'] = {
    #     'browser': 'ALL',
    # #    'performance': 'ALL',
    # }
    driver = driver_litecart(desired_capabilities=caps)

    result = True
    try:

        driver.get(url='http://localhost/litecart/admin/')
        driver.login()
        driver.click_on_catalog()
        driver.open_all_closed_folders()

        links = driver.get_links_for_all_products()
        print('\nСтраницы товаров:')
        # считываем текущий лог (для очистки)
        driver.get_log('browser')

        for link in links:
            print('==', link)
            driver.get(url=link)
            logs = driver.get_log('browser')
            if len(logs) > 0:
                result = False
                pprint(logs)

        # for link in links:
        #     print('==', link)
        #     f = 'a[href="' + link + '"]'
        #     driver.find_element(By.CSS_SELECTOR, f).click()
        #     item = WebDriverWait(driver=driver,
        #                          timeout=10).until(EC.element_to_be_clickable((By.NAME, 'cancel')))
        #     driver.find_element(By.NAME, 'cancel').click()
        #     logs = driver.get_log('browser')
        #     result = result and (len(logs) == 0)
        #     print('browser log:', logs)

    except Exception as ex:
        result = False
        print(f"Exception: {type(ex).__name__}")
        print(ex)
        # если упали, то делаем скриншот, сохраняется в текущей папке
        driver.save_screenshot('scr_' + datetime.now().strftime('%Y%m%d%H%M%S') + '.png')

    finally:
        print('\nРезультат теста:', 'Пройден успешно' if result else '!!! Ошибка !!!', '\n')
        driver.quit()
