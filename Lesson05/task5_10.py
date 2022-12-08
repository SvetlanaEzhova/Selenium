''' Сделайте сценарий, который проверяет, что при клике на товар открывается правильная страница товара в учебном приложении litecart.

Более точно, нужно открыть главную страницу, выбрать первый товар в блоке Campaigns и проверить следующее:

а) на главной странице и на странице товара совпадает текст названия товара
б) на главной странице и на странице товара совпадают цены (обычная и акционная)
в) обычная цена зачёркнутая и серая (можно считать, что "серый" цвет это такой, у которого в RGBa представлении одинаковые значения для каналов R, G и B)
г) акционная жирная и красная (можно считать, что "красный" цвет это такой, у которого в RGBa представлении каналы G и B имеют нулевые значения)
(цвета надо проверить на каждой странице независимо, при этом цвета на разных страницах могут не совпадать)
д) акционная цена крупнее, чем обычная (это тоже надо проверить на каждой странице независимо)

Необходимо убедиться, что тесты работают в разных браузерах, желательно проверить во всех трёх ключевых браузерах (Chrome, Firefox, Edge). '''

import sys
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class price:
    ''' под класс со всеми необходимыми полями для цены'''

    def __init__(
        self,
        value: float = 0,    # цена
        size: float = 0,    # размер шрифта
        weight: int = 0,    # Насыщенность шрифта от 100 до 900
        color: list = [],    # цвет : массив из 3 или 4 цифр
        text_decoration_line: str = None    # зачеркнутый шрифт или нет
    ) -> None:
        self.value = value
        self.size = size
        self.weight = weight
        self.color = color
        self.text_decoration_line = text_decoration_line

    def fill_fields(self, wb, css_selector):
        __item = wb.find_element(By.CSS_SELECTOR, css_selector)
        self.value = self.__conv_to_float(__item.text)
        self.color = self.__conv_to_list(__item.value_of_css_property('color'))
        self.size = self.__conv_to_float(__item.value_of_css_property('font-size'))
        self.weight = int(__item.value_of_css_property('font-weight'))
        self.text_decoration_line = __item.value_of_css_property('text-decoration-line')

    def __conv_to_float(self, st: str) -> float:
        return float(re.sub('[^0-9.]', '', st))

    def __conv_to_list(self, st: str) -> list:
        return list(map(int, re.sub('[^0-9.,]', '', st).split(',')))

    def __repr__(self) -> str:
        return f'( value={self.value}, size={self.size}, weight={self.weight}, color={self.color}, text_decoration_line={self.text_decoration_line})'


class CardProduct:
    ''' Класс со всеми необходимыми полями для товара: наименование товара и две цены (см отдельный класс price выше)'''

    def __init__(
        self, name: str = None, regular_price: price = None, campaign_price: price = None
    ) -> None:
        self.name = name    # наименование товара
        self.regular_price = price() if regular_price is None else regular_price
        self.campaign_price = price() if campaign_price is None else campaign_price

    def fill_prices(self, wb):
        self.regular_price.fill_fields(wb, 'div.price-wrapper > *:first-child')
        self.campaign_price.fill_fields(wb, 'div.price-wrapper > *:last-child')

    def __repr__(self) -> str:
        return f'( name={self.name},\n   regular_price={self.regular_price},\n   campaign_price={self.campaign_price})'


def init_driver(br: str = 'chrome'):
    ''' Возвращает webdriver для указанного браузера'''

    print('\nБраузер:', br, '\n')
    if br.upper() in ['CHROME', 'CH']:
        return webdriver.Chrome()
    if br.upper() in ['EDGE', 'MEDGE']:
        return webdriver.Edge()
    if br.upper() in ['FIREFOX', 'FF']:
        options = Options()
        options.binary_location = r'C:\\Program Files\\Mozilla Firefox\\firefox.exe'
        return webdriver.Firefox(options=options)


if __name__ == "__main__":
    driver = init_driver(sys.argv[1] if len(sys.argv) > 1 else 'chrome')

    result = True
    try:
        driver.get(url="http://localhost/litecart/")

        item = driver.find_element(By.CSS_SELECTOR, 'div#box-campaigns li:nth-of-type(1)')

        # Собираем все необходимые данные по товару с главной страницы
        p1 = CardProduct()
        p1.name = item.find_element(By.CSS_SELECTOR, 'div.name').text
        p1.fill_prices(item)
        print('Товар на главной странице:\n', p1)

        item.click()
        # просто, чтобы убедиться, что данные с ценой успели загрузиться после перехода на новую страницу сайта
        WebDriverWait(driver=driver, timeout=5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.price-wrapper'))
        )

        #  Собираем все необходимые данные по товару с карточки товара
        p2 = CardProduct()
        p2.name = driver.find_element(By.CSS_SELECTOR, 'h1.title').text
        p2.fill_prices(driver)
        print('Товар на странице товара:\n', p2)

        # Сравнениваем полученные выше результаты:
        # а) на главной странице и на странице товара совпадает текст названия товара
        if p1.name != p2.name:
            result = False
            print(f'Названия не совпадают: {p1.name} != {p2.name}')

        # б) на главной странице и на странице товара совпадают цены (обычная и акционная)
        if p1.regular_price.value != p2.regular_price.value:
            result = False
            print(
                f'Обычные цены не совпадают: {p1.regular_price.value} != {p2.regular_price.value}'
            )

        if p1.campaign_price.value != p2.campaign_price.value:
            result = False
            print(
                f'Акционные цены не совпадают: {p1.campaign_price.value} != {p2.campaign_price.value}'
            )

        # в) обычная цена зачёркнутая и серая (можно считать, что "серый" цвет это такой, у которого в RGBa представлении одинаковые значения для каналов R, G и B)
        if p1.regular_price.text_decoration_line != 'line-through':
            result = False
            print(f'Обычная цена на главной странице не зачеркнута')

        if p2.regular_price.text_decoration_line != 'line-through':
            result = False
            print(f'Обычная цена на странице товара не зачеркнута')

        if not (
            p1.regular_price.color[0] == p1.regular_price.color[1] == p1.regular_price.color[2]
        ):
            result = False
            print(f'Обычная цена на главной странице не серая ')

        if not (
            p2.regular_price.color[0] == p2.regular_price.color[1] == p2.regular_price.color[2]
        ):
            result = False
            print(f'Обычная цена на странице товара не серая ')

        # г) акционная жирная и красная (можно считать, что "красный" цвет это такой, у которого в RGBa представлении каналы G и B имеют нулевые значения)
        if p1.campaign_price.weight < 700:    # firefox вернул 900, а не 700 как другие. Все что от 700 и выше, можно считать жирным, поэтому < 700, а не != 700
            result = False
            print(f'Акционная цена на главной странице не bold')

        if p2.campaign_price.weight < 700:
            result = False
            print(f'Акционная цена на странице товара не bold')

        if not (p1.campaign_price.color[1] == p1.campaign_price.color[2] == 0):
            result = False
            print(f'Акционная цена на главной странице не красная ')

        if not (p2.campaign_price.color[1] == p2.campaign_price.color[2] == 0):
            result = False
            print(f'Акционная цена на странице товара не красная ')

        # д) акционная цена крупнее, чем обычная (это тоже надо проверить на каждой странице независимо)
        if p1.campaign_price.size <= p1.regular_price.size:
            result = False
            print(f'Акционная цена на главной странице НЕ крупнее, чем обычная')

        if p2.campaign_price.size <= p2.regular_price.size:
            result = False
            print(f'Акционная цена на странице товара НЕ крупнее, чем обычная')

    except Exception as ex:
        result = False
        print(f"Exception: {type(ex).__name__}")
        print(ex)
    finally:
        print('\nРезультат теста:', 'Пройден успешно' if result else '!!! Ошибка !!!', '\n')
        driver.quit()
