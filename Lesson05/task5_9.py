''' Сделайте сценарии, который на странице http://localhost/litecart/admin/?app=geo_zones&doc=geo_zones 
заходит в каждую из стран и проверяет, что зоны расположены в алфавитном порядке. '''

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException


class driver_litecart_admin(webdriver.Chrome):

    def login_to_litecart_admin(
        self,
        url: str = 'http://localhost/litecart/admin/',
        user: str = 'admin',
        password: str = 'admin'
    ) -> None:
        ''' Логинится на указанный ресурс, если не смог, то упадет с TimeoutException '''

        self.get(url=url)
        self.find_element(By.NAME, 'username').send_keys(user)
        self.find_element(By.NAME, 'password').send_keys(password)
        self.find_element(By.NAME, 'login').click()
        # WebDriverWait используется так как перед этим был .click(), приводящий к изменению на странице
        WebDriverWait(driver=self, timeout=5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div#body-wrapper'))
        )


if __name__ == "__main__":
    driver = driver_litecart_admin()
    #driver.implicitly_wait(10)
    result = True
    try:
        driver.login_to_litecart_admin(
            url='http://localhost/litecart/admin/?app=geo_zones&doc=geo_zones'
        )
        # получаем список ссылок для всех стран
        links = [
            item.get_attribute('href') for item in
            driver.find_elements(By.CSS_SELECTOR, 'td#content tr.row td:nth-child(3) a')
        ]
        #print(links)
        for page in links:
            driver.get(url=page)
            print(
                driver.find_element(By.CSS_SELECTOR,
                                    'form input[name=name]').get_attribute('value'),
                end=': '
            )
            # получаем названия всех зон из text
            # option[selected=selected] позволяет исключить заголовок
            # а последняя строка таблицы(footer) не имеет третьей колонки (td:nth-child(3))
            zones = [
                item.text for item in driver.find_elements(
                    By.CSS_SELECTOR, 'table#table-zones td:nth-child(3) option[selected=selected]'
                )
            ]
            compare = zones == sorted(zones)
            print(f'зоны расположены {"" if compare else "НЕ "}в алфавитном порядке')
            result = result and compare
            #print(zones)

    except Exception as ex:
        result = False
        print(f"Exception: {type(ex).__name__}")
        print(ex)
    finally:
        print('\nРезультат теста:', 'Пройден успешно' if result else '!!! Ошибка !!!', '\n')
        driver.quit()
