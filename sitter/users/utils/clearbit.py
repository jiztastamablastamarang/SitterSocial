import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import pandas as pd

LOGIN = 'eugene@beelyk.com'
PASSWORD = 'qwrerwqewЛОЛОЄДОщш224234'

class ClearBit:

    def __init__(self):
        self.timeout = 10
        service = Service(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        # options.add_argument('--headless')
        options.add_argument("--start-maximized")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument("--disable-blink-features=AutomationControlled")
        self.driver = webdriver.Chrome(service=service, options=options)
        self.waiter = WebDriverWait(self.driver, self.timeout)
        self.action = ActionChains(self.driver)
        self.core = "https://clearbit.com/"

    def lookup(self, user, password, email):
        driver = self.driver
        waiter = self.waiter
        driver.get(f"{self.core}login/")
        waiter.until(EC.visibility_of_element_located(
            (By.NAME, "email"))).send_keys(user)
        waiter.until(EC.visibility_of_element_located(
            (By.NAME, "password"))).send_keys(password)
        waiter.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[@type='submit']"))).click()

        # Lookup
        time.sleep(self.timeout)
        driver.get(f"https://dashboard.clearbit.com/lookup")
        form = waiter.until(EC.visibility_of_element_located(
            (By.XPATH, "//input[@type='text']")))
        form.send_keys(email)
        form.send_keys(Keys.RETURN)
        time.sleep(self.timeout//5)
        try:
            expand = driver.find_element(By.CLASS_NAME, "expand")
            if expand:
                expand.click()
        except:
            pass
        # Get details
        details = dict()
        for chunk in ["summary", "detail-data"]:
            elements = waiter.until(EC.visibility_of_element_located((By.CLASS_NAME, chunk)))
            keys = [key.text for key in elements.find_elements(By.TAG_NAME, "h4")]
            values = [value.text for value in elements.find_elements(By.TAG_NAME, "p")]
            element_dict = dict(zip(keys, values))
            details.update(element_dict)

        return details


def email_details(query):
    driver = ClearBit()
    return driver.lookup(LOGIN, PASSWORD, query)


def main():
    start = time.time()
    query = 'shop@muztorg.ua'
    data = pd.Series(email_details(query))
    print(data)
    end = time.time()
    print(f'{end - start}')

if __name__ == "__main__":
    main()
