''' просто рабочий пример по логированию на питоне 3.10 селениюм 4.5 хромдрайвер 108.0.5359'''

from datetime import datetime
from selenium import webdriver
import pprint    # печатает читабельный вид json

if __name__ == "__main__":

    # enable browser logging
    caps = webdriver.DesiredCapabilities.CHROME.copy()
    caps['goog:loggingPrefs'] = {
        'browser': 'ALL',
        'performance': 'ALL',
    }

    # OFF: Логгирование отключено
    # SEVERE: Сообщения об ошибках. К примеру, при неизвестной команде.   <--- похоже это по умолчанию !!!
    # WARNING: Предупреждения о том, что могло быть неверным, хоть ситуация и было успешно обработано. Например, перехваченное исключение.
    # INFO: Сообщения информативного характера. Например, о полученных командах.
    # DEBUG: Сообщения для дебаггинга. Например, информация о состоянии драйвера.
    # ALL: Все сообщения. Это способ получить все сообщения независимо от его уровня.

    options = webdriver.ChromeOptions()
    # options.add_argument('log-level=2')

    # log-level: Sets the minimum log level. Valid values are from 0 to 3:
    # INFO = 0,
    # WARNING = 1,
    # LOG_ERROR = 2,
    # LOG_FATAL = 3.
    # default is 0.
    # set 2 to avoid the error messages like :
    # [46220:6804:1223/163145.199:ERROR:ssl_client_socket_impl.cc(982)] handshake failed; returned -1, SSL error code 1, net_error -200
    # set 3 to avoid the error messages like :
    # [39608:52852:1223/163151.142:ERROR:device_event_log_impl.cc(215)] [16:31:51.143] USB: usb_device_handle_win.cc:1045 Failed to read descriptor from node connection: Присоединенное к системе устройство не
    # работает. (0x1F)

    driver = webdriver.Chrome(options=options, desired_capabilities=caps)
    print(driver.log_types)

    result = True
    try:
        driver.get(url='http://localhost/litecart/')
        driver.get(url='https://www.geeksforgeeks.org/')
        #driver.get(url='http://localhost/litecart/admin/?app=catalog&doc=catalog&category_id=1')

        driver.save_screenshot('scr2_' + datetime.now().strftime('%Y%m%d%H%M%S') + '.png')
    except Exception as ex:
        result = False
        print(f"Exception: {type(ex).__name__}")
        print(ex)
        # если упали, то делаем скриншот, сохраняется в текущей папке
        driver.save_screenshot('scr_' + datetime.now().strftime('%Y%m%d%H%M%S') + '.png')

    finally:
        print('\nРезультат теста:', 'Пройден успешно' if result else '!!! Ошибка !!!', '\n')
        print('\nBROWSER:')
        pprint.pprint(driver.get_log('browser'))
        if 'performance' in driver.log_types:
            with open('performance_log.txt', 'w') as f:
                print('\nPERFORMANCE:', driver.get_log('performance'), file=f)

        driver.quit()
