import logging
import time
from typing import Dict, List

import requests 
from classes import Message

from selenium import webdriver
from selenium.common import WebDriverException, SessionNotCreatedException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from constants import COOKIES


logger = logging.getLogger(__name__)
        
CAMPUS_URL = "https://campus0d.unad.edu.co/campus"
class Campus:
    tab_cursos_id = ''
    def __init__(self):
        try:
            self.init_driver()
            self.driver.get(CAMPUS_URL)
            for cookie in COOKIES:
                self.driver.add_cookie(cookie)
            self.driver.get(CAMPUS_URL+"/accesit.php")
            if "accesit.php" not in self.driver.current_url:
                self.login()
            
        except (WebDriverException, SessionNotCreatedException) as e:
            logger.error("Chrome driver failed: ", e)
            raise e
        
    def end(self):
        self.driver.quit()

    def init_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=chrome_options)
        logger.info("Chrome driver started")
        
    def retry_cookies(self):
        for i in range(10):
            failed_div = self.get_element(By.CLASS_NAME, "Cuerpo600")
            if failed_div and failed_div[0].text == 'Acceder a Campus Virtual\nSu navegador no logro procesar las cookies para el sitio unad.edu.co':
                print(f'retriying due to cookies: {i}')
                self.end()
                time.sleep(i)
                self.init_driver()
                self.driver.get(CAMPUS_URL)
                continue
            return
        raise Exception("Failed cookies")

    def login(self):
        global COOKIES 
        self.retry_cookies()
        user_field = self.get_element(By.ID, 'txtuser')[0]
        user_field.send_keys('1022322066')
        button = self.driver.find_element(By.ID, 'cmdIngresa2')
        button.click()

        pass_field = self.driver.find_element(By.ID, 'txtclave2')
        pass_field.send_keys('!sTSjFWT43Wc_Ki')

        button = self.driver.find_element(By.ID, 'cmdIngresa2')
        button.click()
        print('Login succesful')

        self.driver.get('https://campus0d.unad.edu.co/campus/miscursos.php')
        COOKIES += self.driver.get_cookies()

    
    # def get_unreaded_posts(self):
    #     #use find
    #     self.driver.get('https://campus0d.unad.edu.co/campus/miscursos.php')
    #     unread_posts_text = []
    #     time.sleep(1)
    #     cards = self.driver.find_elements(By.CLASS_NAME, "card-curso")[:1]
    #     print('Courses loaded')
    #     for course_card in cards:
    #         button = course_card.find_element(By.TAG_NAME, "button")
    #         button.click()

    #         self.driver.switch_to.window(self.driver.window_handles[-1])
    #         time.sleep(2)
    #         aprendizaje_button = self.driver.find_element(By.ID, "gridsection-2")
    #         aprendizaje_button.click()
    #         time.sleep(1)
    #         unread_elements = self.driver.find_elements(By.CLASS_NAME, "unread")
    #         if len([i.text for i in unread_elements if i.text != ""]) == 0: return []
    #         unread_elements[-1].find_element(By.TAG_NAME, "a").click()

    #         foro = self.driver.find_element(By.CLASS_NAME, "hasunread")
    #         foro.find_element(By.TAG_NAME, "a").click()
            
    #         unread_posts = self.driver.find_elements(By.CLASS_NAME, "unread")
            
    #         for i in unread_posts:
    #             unread_posts_text.append(i.text)
            
    #         self.driver.close()

    #     return unread_posts_text
    
    def get_element(self, by, value, of=None):
        parent = self.driver
        if of:
            parent = of
        
        try:
            wait = WebDriverWait(self.driver, 5)
            wait.until(EC.presence_of_element_located((by, value)))
            return parent.find_elements(by, value)
        except:
            return
        
    def read_courses_email(self):
        self.driver.get(CAMPUS_URL+"/miscursos.php")
        self.tab_cursos_id = self.driver.current_window_handle
        cards = self.get_element(By.CLASS_NAME, "card-curso")

        if not cards:
            raise Exception('🟥 No encontré el div con el listado de cursos')
        
        course_message: Dict[str, List[Message]] = {}
        for i in range(len(cards)):
            course_card = self.driver.find_elements(By.CLASS_NAME, "card-curso")[i]
            button = course_card.find_element(By.TAG_NAME, "button")
            course_id = course_card.find_element(By.TAG_NAME, "b").text
            button.click()
            self.driver.switch_to.window(self.driver.window_handles[-1])

            messages = self.read_email()
            course_message[course_id] = messages
            self.driver.close()
            self.driver.switch_to.window(self.tab_cursos_id)
            self.driver.get(CAMPUS_URL+"/miscursos.php")

        return course_message
    
    def read_email(self):
        email_button = self.get_element(By.ID, "nav-mail-popover-container")[0]
        email_button.click()

        mail_elements = self.get_element(By.CLASS_NAME, "mail-navbar-menu")[0].find_elements(By.TAG_NAME, 'a')
        bandeja = mail_elements[0]
        
        unread = self.get_element(By.TAG_NAME, 'span', bandeja)
        if not unread:
            return []
        
        unread_amount = unread[0].text

        if not bool(unread_amount):
            return []
        
        bandeja.click()
        messages: List[Message] = []
        unread_mesage_divs = self.find(By.CLASS_NAME, 'mail_unread', 0)

        for _ in range(len(unread_mesage_divs)):
            self.get_element(By.CLASS_NAME, 'mail_unread', 0)[0].click()
            mail_div = self.get_element(By.CLASS_NAME, 'mail_content')[0]
            user_from = self.get_element(By.CLASS_NAME, 'user_from')[0]
            date = self.get_element(By.CLASS_NAME, 'mail_date')[0]
            images = self.get_element(By.TAG_NAME, 'img', mail_div)

            messages.append(Message('text', f'{user_from.text} dijo el {date.text}'))

            for image in images:
                if 'icon' in image.get_attribute("class"):
                    continue
                image_bytes = self.get_imgbytes(image.get_attribute('src'))
                messages.append(Message('photo', '', image_bytes))
            messages.append(Message('text', "--------\n\n"+mail_div.text))
            self.find(By.CLASS_NAME, 'mail_goback')[0].click()

        return messages
    
    def get_imgbytes(self, url: str):
        return requests.get(
            url,
            cookies={i['name']: i['value'] for i in self.driver.get_cookies()}
        ).content

    def find(self, by: str, value: str, of: any = 0):
        if of:
            try:
                return of.find_elements(by, value)
            except:
                return
        try:
            return self.driver.find_elements(by, value)
        except:
            return
        