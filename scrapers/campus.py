import logging
import time

from selenium import webdriver
from selenium.common import WebDriverException, SessionNotCreatedException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from constants import COOKIES


logger = logging.getLogger(__name__)


class Campus:

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        # chrome_options.add_argument("--enable-features=Geolocation")
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.delete_all_cookies()
            logger.info("Chrome driver started")
            self.driver.get("https://campus0d.unad.edu.co/campus/miscursos.php")
            self.login()
            
        except (WebDriverException, SessionNotCreatedException) as e:
            logger.error("Chrome driver failed: ", e)
            raise e

    def login(self):
        time.sleep(1)
        failed_div = self.find(By.CLASS_NAME, "Cuerpo600")
        if failed_div and failed_div[0].text == 'Acceder a Campus Virtual\nSu navegador no logro procesar las cookies para el sitio unad.edu.co':
            raise Exception("Failed cookies")
        user_field = self.driver.find_element(By.ID, 'txtuser')
        user_field.send_keys('1022322066')
        button = self.driver.find_element(By.ID, 'cmdIngresa2')
        button.click()

        pass_field = self.driver.find_element(By.ID, 'txtclave2')
        pass_field.send_keys('!sTSjFWT43Wc_Ki')

        button = self.driver.find_element(By.ID, 'cmdIngresa2')
        button.click()
        print('Login succesful')
        global COOKIES 
        COOKIES += self.driver.get_cookies()

        self.driver.get('https://campus0d.unad.edu.co/campus/miscursos.php')

        
    def get_courses(self):
        cards = self.driver.find_elements(By.CLASS_NAME, "card-curso")
        print([card.text for card in cards])
    
    def get_unreaded_posts(self):
        self.driver.get('https://campus0d.unad.edu.co/campus/miscursos.php')
        unread_posts_text = []
        time.sleep(1)
        cards = self.driver.find_elements(By.CLASS_NAME, "card-curso")
        print('Courses loaded')
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
    
    def read_courses_email(self):
        self.driver.get('https://campus0d.unad.edu.co/campus/miscursos.php')

        time.sleep(1)
        cards = self.driver.find_elements(By.CLASS_NAME, "card-curso")

        course_message = {}
        for i in range(len(cards)):
            time.sleep(1)
            course_card = self.driver.find_elements(By.CLASS_NAME, "card-curso")[i]
            button = course_card.find_element(By.TAG_NAME, "button")
            course_id =course_card.find_element(By.TAG_NAME, "b").text
            button.click()
            self.driver.switch_to.window(self.driver.window_handles[-1])
            time.sleep(2)
            messages = self.read_email()
            course_message[course_id] = messages
            self.driver.get('https://campus0d.unad.edu.co/campus/miscursos.php')

        return course_message
    
    def read_email(self):
        email_button = self.driver.find_element(By.ID, "nav-mail-popover-container")
        email_button.click()

        mail_elements = self.driver.find_element(By.CLASS_NAME, "mail-navbar-menu").find_elements(By.TAG_NAME, 'a')
        bandeja = mail_elements[0]
        # ???
        unread = self.find(By.TAG_NAME, 'span', bandeja)
        if not unread:
            return []
        
        unread_amount = unread[0].text

        if not bool(unread_amount):
            return []
        
        bandeja.click()
        messages = []
        unread_mesage_divs = self.find(By.CLASS_NAME, 'mail_unread', 0)
        for _ in range(len(unread_mesage_divs)):
            time.sleep(1)
            self.find(By.CLASS_NAME, 'mail_unread', 0)[0].click()
            time.sleep(2)
            messages.append("--------\n\n"+self.find(By.CLASS_NAME, 'mail_content')[0].text)
            self.find(By.CLASS_NAME, 'mail_goback')[0].click()
            time.sleep(1)

        return messages



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
            

    