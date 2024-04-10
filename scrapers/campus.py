import logging
import time

from selenium import webdriver
from selenium.common import WebDriverException, SessionNotCreatedException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# from constants import COOKIES

logger = logging.getLogger(__name__)


class Campus:

    def __init__(self):
        chrome_options = Options()
        # chrome_options.add_argument("--no-sandbox")
        # chrome_options.add_argument("--headless")
        # chrome_options.add_argument("--disable-dev-shm-usage")
        

        try:
            import os
            self.driver = webdriver.ChromiumEdge()
            self.driver.delete_all_cookies()
            logger.info("Chrome driver started")
            self.driver.get("https://campus0d.unad.edu.co/campus/miscursos.php")
            self.login()
            
        except (WebDriverException, SessionNotCreatedException) as e:
            logger.error("Chrome driver failed: ", e)
            raise e

    def login(self):
        user_field = self.driver.find_element(By.ID, 'txtuser')
        user_field.send_keys('1022322066')
        button = self.driver.find_element(By.ID, 'cmdIngresa2')
        button.click()

        pass_field = self.driver.find_element(By.ID, 'txtclave2')
        pass_field.send_keys('!sTSjFWT43Wc_Ki')

        button = self.driver.find_element(By.ID, 'cmdIngresa2')
        button.click()

        # COOKIES.update(self.driver.get_cookies())

        self.driver.get('https://campus0d.unad.edu.co/campus/miscursos.php')

        
    def get_courses(self):
        cards = self.driver.find_elements(By.CLASS_NAME, "card-curso")
        print([card.text for card in cards])
    
    def get_unreaded_posts(self):
        self.driver.get('https://campus0d.unad.edu.co/campus/miscursos.php')
        unread_posts_text = []
        time.sleep(1)
        cards = self.driver.find_elements(By.CLASS_NAME, "card-curso")
        for course_card in cards:
            button = course_card.find_element(By.TAG_NAME, "button")
            button.click()

            self.driver.switch_to.window(self.driver.window_handles[-1])
            time.sleep(2)
            aprendizaje_button = self.driver.find_element(By.ID, "gridsection-2")
            aprendizaje_button.click()
            time.sleep(1)
            unread_elements = self.driver.find_elements(By.CLASS_NAME, "unread")
            if len([i.text for i in unread_elements if i.text != ""]) == 0: return []
            unread_elements[-1].find_element(By.TAG_NAME, "a").click()

            foro = self.driver.find_element(By.CLASS_NAME, "hasunread")
            foro.find_element(By.TAG_NAME, "a").click()
            
            unread_posts = self.driver.find_elements(By.CLASS_NAME, "unread")
            
            for i in unread_posts:
                unread_posts_text.append(i.text)
            
            self.driver.close()

        return unread_posts_text
    