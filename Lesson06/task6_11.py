''' Сделайте сценарий для регистрации нового пользователя в учебном приложении litecart (не в админке, а в клиентской части магазина).

Сценарий должен состоять из следующих частей:

1) регистрация новой учётной записи с достаточно уникальным адресом электронной почты (чтобы не конфликтовало с 
ранее созданными пользователями, в том числе при предыдущих запусках того же самого сценария),
2) выход (logout), потому что после успешной регистрации автоматически происходит вход,
3) повторный вход в только что созданную учётную запись,
4) и ещё раз выход.

В качестве страны выбирайте United States, штат произвольный. При этом формат индекса -- пять цифр.

Можно оформить сценарий либо как тест, либо как отдельный исполняемый файл.

Проверки можно никакие не делать, только действия -- заполнение полей, нажатия на кнопки и ссылки. 
Если сценарий дошёл до конца, то есть созданный пользователь смог выполнить вход и выход -- значит создание прошло успешно.

В форме регистрации есть капча, её нужно отключить в админке учебного приложения на вкладке Settings -> Security. '''

from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys


class User:
    ''' структура со всеми полями и значениями по умолчанию для пользователя'''

    def __init__(
        self,
        firstname: str = 'John',
        lastname: str = 'Doe',
        address: str = 'somewhere',
        postcode: str = '12345',
        city: str = 'San Jose',
        country: str = 'United States',
        zone: str = 'California',
        phone: str = '+11231234567',
        email: str = 'user@domain.com',
        password: str = 'password'
    ) -> None:
        self.firstname = firstname
        self.lastname = lastname
        self.address = address
        self.postcode = postcode
        self.city = city
        self.country = country
        self.zone = zone
        self.phone = phone
        self.email = email
        self.password = password


class driver_litecart(webdriver.Chrome):
    ''' класс с create\logout\login'''

    def create_new_user(self, user: User):
        ''' Нажимаем "Создать нового пользователя", заполняем все требуемые поля и нажимаем "Создать" '''

        self.find_element(By.CSS_SELECTOR, 'div#box-account-login a[href*=create_account]').click()
        WebDriverWait(driver=self,
                      timeout=5).until(EC.presence_of_element_located((By.NAME, 'create_account')))

        self.find_element(By.NAME, 'firstname').send_keys(user.firstname)
        self.find_element(By.NAME, 'lastname').send_keys(user.lastname)
        self.find_element(By.NAME, 'address1').send_keys(user.address)
        self.find_element(By.NAME, 'postcode').send_keys(user.postcode)
        self.find_element(By.NAME, 'city').send_keys(user.city)

        self.find_element(By.CLASS_NAME, 'selection').click()
        self.find_element(By.CLASS_NAME,
                          'select2-search__field').send_keys(user.country + Keys.ENTER)

        self.find_element(By.CSS_SELECTOR,
                          'select[name=zone_code]').send_keys(user.zone + Keys.ENTER)

        self.find_element(By.NAME, 'email').send_keys(user.email)
        self.find_element(By.NAME, 'phone').send_keys(user.phone)

        self.find_element(By.NAME, 'password').send_keys(user.password)
        self.find_element(By.NAME, 'confirmed_password').send_keys(user.password)

        self.find_element(By.NAME, 'create_account').click()
        WebDriverWait(driver=self,
                      timeout=5).until(EC.presence_of_element_located((By.ID, 'box-account')))

    def login(self, user: User):
        ''' Нажимаем "Домой", заполняем email\пароль и нажимаем "Логин" '''

        self.find_element(By.ID, 'logotype-wrapper').click()
        WebDriverWait(driver=self, timeout=5).until(
            EC.presence_of_element_located((By.ID, 'box-account-login'))
        )

        self.find_element(By.NAME, 'email').send_keys(user.email)
        self.find_element(By.NAME, 'password').send_keys(user.password)

        self.find_element(By.NAME, 'login').click()
        WebDriverWait(driver=self,
                      timeout=5).until(EC.presence_of_element_located((By.ID, 'box-account')))

    def logout(self):
        ''' Нажимаес "Logout" '''

        self.find_element(By.CSS_SELECTOR, 'div#box-account a[href*=logout]').click()
        WebDriverWait(driver=self, timeout=15).until(
            EC.presence_of_element_located((By.ID, 'box-account-login'))
        )


if __name__ == "__main__":

    driver = driver_litecart()

    # пользователь с с достаточно уникальным email (dd<ДатаЧасыМинутыСекунды>@mail.com)
    user = User(email='dd' + datetime.now().strftime('%d%H%M%S') + '@mail.com')
    result = True

    try:
        driver.get(url="http://localhost/litecart/")
        driver.create_new_user(user)
        driver.logout()
        driver.login(user)
        driver.logout()

    except Exception as ex:
        result = False
        print(f"Exception: {type(ex).__name__}")
        print(ex)
        # если упали, то делаем скриншот, сохраняется в текущей папке
        driver.save_screenshot('scr_' + datetime.now().strftime('%Y%m%d%H%M%S') + '.png')

    finally:
        print('\nРезультат теста:', 'Пройден успешно' if result else '!!! Ошибка !!!', '\n')
        driver.quit()
