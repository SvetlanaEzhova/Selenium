''' Сделайте сценарий для учебного приложения litecart, который на 
странице http://localhost/litecart/admin/?app=countries&doc=countries
а) проверяет, что страны расположены в алфавитном порядке
б) для тех стран, у которых количество зон отлично от нуля - открывает 
страницу этой страны и там проверяет, что геозоны расположены в алфавитном порядке '''

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
            url='http://localhost/litecart/admin/?app=countries&doc=countries'
        )
        # получаем названия (text) всех стран
        countries = [
            item.text for item in
            driver.find_elements(By.CSS_SELECTOR, 'td#content tr.row td:nth-child(5) a')
        ]
        # сравниваем оригинал и отсортированный список
        compare = countries == sorted(countries)
        print(f'Страны расположены {"" if compare else "НЕ "}в алфавитном порядке')
        result = result and compare

        # получаем список ссылок для стран, у которых кол-во зон не равно 0
        links_with_zones = [
            item.find_element(By.CSS_SELECTOR, 'td:nth-child(5) a').get_attribute('href')
            for item in driver.find_elements(By.CSS_SELECTOR, 'td#content tr.row')
            if item.find_element(By.CSS_SELECTOR, 'td:nth-child(6)').text != '0'
        ]
        print(links_with_zones)
        for page in links_with_zones:
            driver.get(url=page)
            print(
                driver.find_element(By.CSS_SELECTOR,
                                    'form input[name=name]').get_attribute('value'),
                end=': '
            )
            # получаем названия всех зон
            # :not(.header) - это выкинули заголовок таблицы,
            # [type=hidden] - отсекли последнюю строку для ввода новых зон)
            zones = [
                item.get_attribute('value') for item in driver.find_elements(
                    By.CSS_SELECTOR,
                    'table#table-zones tr:not(.header) td:nth-child(3) input[type=hidden]'
                )
            ]
            # print(zones)
            compare = zones == sorted(zones)
            print(f'геозоны расположены {"" if compare else "НЕ "}в алфавитном порядке')
            result = result and compare

    except Exception as ex:
        result = False
        print(f"Exception: {type(ex).__name__}")
        print(ex)
    finally:
        print('\nРезультат теста:', 'Пройден успешно' if result else '!!! Ошибка !!!', '\n')
        driver.quit()
