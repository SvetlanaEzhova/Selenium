''' Сделайте сценарий, который проверяет, что ссылки на странице редактирования страны открываются в новом окне.

Сценарий должен состоять из следующих частей:

1) зайти в админку
2) открыть пункт меню Countries (или страницу http://localhost/litecart/admin/?app=countries&doc=countries)
3) открыть на редактирование какую-нибудь страну или начать создание новой
4) возле некоторых полей есть ссылки с иконкой в виде квадратика со стрелкой -- они ведут на внешние страницы 
и открываются в новом окне, именно это и нужно проверить.

Конечно, можно просто убедиться в том, что у ссылки есть атрибут target="_blank". Но в этом упражнении требуется 
именно кликнуть по ссылке, чтобы она открылась в новом окне, потом переключиться в новое окно, закрыть его, 
вернуться обратно, и повторить эти действия для всех таких ссылок.

Не забудьте, что новое окно открывается не мгновенно, поэтому требуется ожидание открытия окна. '''

from datetime import datetime
from random import randint

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

    def click_edit_random_country(self):
        '''  Кликаем на Countries в столбце слева, ждем обновления содержимого страницы, 
        нажимаем открываем на редактирования случайную страну и ждем возможности редактировать данные'''

        self.find_element(By.ID, 'box-apps-menu').find_element(By.LINK_TEXT, 'Countries').click()
        WebDriverWait(driver=self,
                      timeout=10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'dataTable')))

        items = self.find_elements(By.CSS_SELECTOR, 'td > a[title=Edit]')
        rand_index = randint(0, len(items) - 1)
        items[rand_index].click()
        WebDriverWait(driver=self,
                      timeout=10).until(EC.visibility_of_element_located((By.NAME, 'phone_code')))
        print('\nСтрана:', self.find_element(By.NAME, 'name').get_attribute('value'))

    def click_on_all_external_links(self):
        ''' Кликаем на все внешние ссылки на странице '''

        links = driver.find_elements(By.CSS_SELECTOR, 'td#content form a[target=_blank')
        print('  всего линков:', len(links))
        main_window = self.current_window_handle
        old_windows = self.window_handles
        for link in links:
            print('    ==', link.get_attribute('href'))
            link.click()
            WebDriverWait(driver=self, timeout=5).until(EC.new_window_is_opened(old_windows))
            #diff_windows = list(set(old_windows) ^ set(self.window_handles))
            diff_windows = list(set(self.window_handles).symmetric_difference(set(old_windows)))
            self.switch_to.window(diff_windows[0])
            self.close()
            self.switch_to.window(main_window)


if __name__ == "__main__":
    driver = driver_litecart()

    result = True
    try:
        driver.get(url='http://localhost/litecart/admin/')
        driver.login()

        driver.click_edit_random_country()
        driver.click_on_all_external_links()

    except Exception as ex:
        result = False
        print(f"Exception: {type(ex).__name__}")
        print(ex)
        # если упали, то делаем скриншот, сохраняется в текущей папке
        driver.save_screenshot('scr_' + datetime.now().strftime('%Y%m%d%H%M%S') + '.png')

    finally:
        print('\nРезультат теста:', 'Пройден успешно' if result else '!!! Ошибка !!!', '\n')
        driver.quit()
