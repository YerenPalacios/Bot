import logging
from typing import Dict, List

from selenium.common import WebDriverException, SessionNotCreatedException
from selenium.webdriver.common.by import By

from classes import Message
from scrapers.drivers.CampusDriver import CampusDriver


logger = logging.getLogger(__name__)
        

class Campus:
    tab_cursos_id = ''
    def __init__(self):
        try:
            self.driver = CampusDriver()
            self.driver.go_to_campus()
            
        except (WebDriverException, SessionNotCreatedException) as e:
            logger.error("Chrome driver failed: ", e)
            raise e
        
    def end(self):
        self.driver.driver.quit()

    
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
    
    
        
    def read_courses_email(self):
        self.driver.go_to("/miscursos.php")
        # self.tab_cursos_id = self.driver.current_window_handle
        first_courses_group = self.driver.get_element(By.CLASS_NAME, 'list__cursos')
        if not first_courses_group:
            raise Exception('🟥 No encontré el div con el listado de cursos')
        
        cards = self.driver.get_elements(By.CLASS_NAME, "card-curso", first_courses_group)

        if not cards:
            raise Exception('🟥 No encontré ningun curso')
        
        course_message: Dict[str, List[Message]] = {}
        
        for i in range(len(cards)):
            course_card = self.driver.get_elements(By.CLASS_NAME, "card-curso")[i]
            course_id = course_card.find_element(By.TAG_NAME, "b").text
            button = course_card.find_element(By.TAG_NAME, "button")
            button.click()
            self.driver.go_to_last_tab()
            
            messages = self.read_email()
            course_message[course_id] = messages
            self.driver.go_to("/miscursos.php")
            
        return course_message
    
    def read_email(self):
        try:
            self.driver.find_element(By.CLASS_NAME, 'closebutton').click()
        except:
            pass
        email_button = self.driver.get_element(By.ID, "nav-mail-popover-container")
        email_button.click()

        mail_elements = self.driver.get_element(By.CLASS_NAME, "mail-navbar-menu").find_elements(By.TAG_NAME, 'a')
        bandeja = mail_elements[0]
        
        unread = self.driver.get_element(By.TAG_NAME, 'span', bandeja)
        if not unread:
            return []
        
        unread_amount = unread.text

        if not bool(unread_amount):
            return []
        
        bandeja.click()
        messages: List[Message] = []
        unread_mesage_divs = self.driver.get_elements(By.CLASS_NAME, 'mail_unread', 0)

        for _ in range(len(unread_mesage_divs)):
            self.driver.get_element(By.CLASS_NAME, 'mail_unread').click()
            mail_div = self.driver.get_element(By.CLASS_NAME, 'mail_content')

            user_from = self.driver.get_element(By.CLASS_NAME, 'user_from')
            date = self.driver.get_element(By.CLASS_NAME, 'mail_date')

            images = self.driver.get_elements(By.TAG_NAME, 'img', mail_div) or []

            messages.append(Message('text', f'{user_from.text} dijo el {date.text}'))

            for image in images:
                if 'icon' in image.get_attribute("class"):
                    continue
                image_bytes = self.driver.get_image(image.get_attribute("src"))
                messages.append(Message('photo', '', image_bytes))
            messages.append(Message('text', "✉️✉️✉️\n\n"+mail_div.text))
            try:
                self.driver.get_element(By.CLASS_NAME, 'mail_goback')[0].click()
            except:
                self.driver.refresh()

        return messages
    