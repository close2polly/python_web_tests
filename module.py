import time
import yaml
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

with open("selenium.yaml") as f:
    config = yaml.safe_load(f)

service = Service(config["driver"])
options = webdriver.ChromeOptions()


class Site:
    def __init__(self, address):
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.maximize_window()
        self.driver.get(address)
        time.sleep(config["sleep_time"])

    def find_element(self, mode, path):
        if mode == "css":
            element = self.driver.find_element(By.CSS_SELECTOR, path)
        elif mode == "xpath":
            element = self.driver.find_element(By.XPATH, path)
        else:
            element = None

        return element

    def close(self):
        self.driver.close()

    def wait_element(self, path):
        try:
            element = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, path))
            )
            return element
        finally:
            print("Error!")
    
    def wait_element_css(self, path):
        try:
            element = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, path))
            )
            return element
        finally:
            print("Error!")


