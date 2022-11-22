from selenium import webdriver
from selenium.webdriver.common.by import By


def admin_login_litecart(user: str = "admin", password: str = "password") -> None:
    driver = webdriver.Chrome()
    try:
        driver.get(url="http://localhost/litecart/admin/")
        driver.find_element(By.NAME, 'username').send_keys(user)
        driver.find_element(By.NAME, 'password').send_keys(password)
        driver.find_element(By.NAME, 'login').click()
    except Exception as ex:
        print(f"Exception: {type(ex).__name__}")
        print(ex)
    finally:
        driver.quit()


if __name__ == "__main__":
    admin_login_litecart()