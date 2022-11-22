from selenium import webdriver

if __name__ == "__main__":
    driver = webdriver.Chrome()
    driver.get(url="https:\\google.com")
    driver.quit()