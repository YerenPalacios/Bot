import time
import logging
from random import uniform
from typing import Dict, List

from selenium import webdriver
from selenium.common import NoSuchElementException, WebDriverException, SessionNotCreatedException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

logger = logging.getLogger(__name__)

cookies = {}

class Campus:

    def __init__(self):
        chrome_options = Options()
        # chrome_options.add_argument("--no-sandbox")
        # chrome_options.add_argument("--headless")
        # chrome_options.add_argument("--disable-dev-shm-usage")
        

        try:
            self.driver = webdriver.Chrome()
            logger.info("Chrome driver started")
            self.driver.get("https://campus0d.unad.edu.co/campus/miscursos.php")
            self.login()
            
        except (WebDriverException, SessionNotCreatedException) as e:
            logger.error("Chrome driver failed: ", e)

    def login(self):
        user_field = self.driver.find_element(By.ID, 'txtuser')
        user_field.send_keys('1022322066')
        button = self.driver.find_element(By.ID, 'cmdIngresa2')
        button.click()

        pass_field = self.driver.find_element(By.ID, 'txtclave2')
        pass_field.send_keys('!sTSjFWT43Wc_Ki')

        button = self.driver.find_element(By.ID, 'cmdIngresa2')
        button.click()

        cookies = self.driver.get_cookies()

        self.driver.get('https://campus0d.unad.edu.co/campus/miscursos.php')

        
    def get_courses(self):
        cards = self.driver.find_elements(By.CLASS_NAME, "card-curso")
        print([card.text for card in cards])
    