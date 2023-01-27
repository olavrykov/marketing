import os
from time import sleep
from selenium.webdriver.common.by import By

#BROWSER = 'Firefox'
BROWSER = 'Chrome'
USE_DEPRECATED_PATH = False

if BROWSER == 'Chrome':
    from selenium.webdriver import Chrome as webdriverBrowser
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager as DriverManager
elif BROWSER == 'Edge':
    from selenium.webdriver import Edge as webdriverBrowser
    from selenium.webdriver.edge.options import Options
    from selenium.webdriver.edge.service import Service
    from webdriver_manager.microsoft import EdgeChromiumDriverManager as DriverManager
elif BROWSER == 'Firefox':
    from selenium.webdriver import Firefox as webdriverBrowser
    from selenium.webdriver.firefox.options import Options
    from selenium.webdriver.firefox.service import Service
    from webdriver_manager.firefox import GeckoDriverManager as DriverManager
else:
    error

class Driver(webdriverBrowser):
    def __init__(self):
#        os.environ['WDM_LOG'] = '0'
#        os.environ['WDM_LOG_LEVEL'] = '0'
        options = Options()
        options.add_argument('--disable-logging') 

        if BROWSER == 'Chrome':
            os.system('taskkill /IM Chrome.exe /T /F')
            profile = f'--user-data-dir={os.environ["LOCALAPPDATA"]}\\Google\\Chrome\\User Data'
        elif BROWSER == 'Firefox':
            os.system('taskkill /IM Firefox.exe /T /F')
            profile = f'--profile {os.environ["APPDATA"]}\\Mozilla\\Firefox\\Profiles\\sixxkrcf.default-release'
        options.add_argument(profile)

#        options.log.level = 'fatal'
#        options.add_argument('--headless')
        #options.add_experimental_option("excludeSwitches", ["enable-automation"])
        #options.add_experimental_option('useAutomationExtension', False)
#        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        service = Service(DriverManager().install())

        if USE_DEPRECATED_PATH:
#            webdriverBrowser.__init__(self, executable_path=service.path)#for old driver
            webdriverBrowser.__init__(self, executable_path=service.path, options=options)
        else:
            webdriverBrowser.__init__(self, service=service, options=options)

        if BROWSER == 'Chrome':
            #Deleay required to fix startup bug in Selenium
            sleep(10)

    def get(self, *arg):
        super().get(*arg)
        sleep(3)

if __name__ == '__main__':
    driver = Driver()
    driver.get('https://rozetka.com.ua/search/?text=video')
#    driver.get('https://www.example.com')
    list_art = driver.find_element(By.CLASS_NAME, 'catalog-grid')
    print(list_art)
    list_art = driver.find_elements(By.CLASS_NAME, 'catalog-grid')
    print(list_art)
    driver.close()
