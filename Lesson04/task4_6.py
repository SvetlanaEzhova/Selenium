''' Сделайте сценарий, который выполняет следующие действия в учебном приложении litecart.
1) входит в панель администратора http://localhost/litecart/admin
2) прокликивает последовательно все пункты меню слева, включая вложенные пункты
3) для каждой страницы проверяет наличие заголовка (то есть элемента с тегом h1) '''

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException


class driver_litecart_admin(webdriver.Chrome):

    def login_to_litecart_admin(self, user: str = "admin", password: str = "admin") -> None:
        ''' Логинится на указанный ресурс, если не смог, то упадет с TimeoutException '''

        self.get(url="http://localhost/litecart/admin/")
        self.find_element(By.NAME, 'username').send_keys(user)
        self.find_element(By.NAME, 'password').send_keys(password)
        self.find_element(By.NAME, 'login').click()
        # WebDriverWait используется так как перед этим был .click(), приводящий к изменению на странице
        WebDriverWait(driver=self, timeout=5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div#body-wrapper'))
        )

    def find_title(self) -> bool:
        ''' Ищет заголовок h1 в правой части экрана. Если не найдет, то сообщит об этом, но не упадет'''

        print('Заголовок:', end=' ')
        try:
            # WebDriverWait используется так как перед этим был .click(), приводящий к изменению на странице
            h1 = WebDriverWait(driver=self, timeout=5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'td#content h1'))
            )
            print(h1.text, end='; ')
            return True
        except TimeoutException:
            print('!!! Отсутствует !!!', end='; ')
            return False


if __name__ == "__main__":
    driver = driver_litecart_admin()
    #driver.implicitly_wait(10)
    result = True
    try:
        driver.login_to_litecart_admin()

        # чтобы использовать FOR, а не WHILE c ожиданием несуществующего элемента
        items = driver.find_elements(By.CSS_SELECTOR, 'ul#box-apps-menu > li')
        for i in range(len(items)):
            print('\nПункт меню слева:', end=' ')
            item = driver.find_element(
                By.CSS_SELECTOR, 'ul#box-apps-menu > li:nth-child(' + str(i + 1) + ')'
            )
            print(item.text, end='; ')
            item.click()
            result = result and driver.find_title()

            # цикл для подменю, если оно есть
            subitems = driver.find_elements(By.CSS_SELECTOR, 'ul.docs > li')
            for j in range(len(subitems)):
                print('\n  Подпункт меню:', end=' ')
                subitem = driver.find_element(
                    By.CSS_SELECTOR, 'ul.docs > li:nth-child(' + str(j + 1) + ')'
                )
                print(subitem.text, end='; ')
                subitem.click()
                result = result and driver.find_title()

    except Exception as ex:
        result = False
        print(f"Exception: {type(ex).__name__}")
        print(ex)
    finally:
        print('\n\nРезультат теста:', 'Пройден успешно' if result else '!!! Ошибка !!!', '\n')
        driver.quit()
