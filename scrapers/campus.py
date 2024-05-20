import logging
from typing import Dict, List

from selenium.common import WebDriverException, SessionNotCreatedException
from selenium.webdriver.common.by import By

from classes import Message
from scrapers.drivers.CampusDriver import CampusDriver


logger = logging.getLogger(__name__)


class Campus:
    tab_cursos_id = ""

    def __init__(self):
        try:
            print("Iniciando driver")
            self.driver = CampusDriver()
            self.driver.go_to_campus()
            print("Driver iniciado")
        except (WebDriverException, SessionNotCreatedException) as e:
            print("Chrome driver failed: ", e)
            raise e

    def end(self):
        self.driver.driver.quit()

    def get_course_cards(self):
        self.driver.go_to("/miscursos.php")
        if "encuesta.php" in self.driver.driver.current_url:
            raise Exception("Toca contestar una encuesta 😒")
        # self.tab_cursos_id = self.driver.current_window_handle
        first_courses_group = self.driver.get_element(By.CLASS_NAME, "list__cursos")
        if not first_courses_group:
            raise Exception("🟥 No encontré el div con el listado de cursos")

        cards = self.driver.get_elements(
            By.CLASS_NAME, "card-curso", first_courses_group
        )

        if not cards:
            raise Exception("🟥 No encontré ningun curso")

        return cards

    def go_to_course(self, i):
        course_card = self.driver.get_elements(By.CLASS_NAME, "card-curso")[i]
        course_id = course_card.find_element(By.TAG_NAME, "b").text.split('\n')[0]
        button = course_card.find_element(By.TAG_NAME, "button")
        button.click()
        self.driver.go_to_last_tab()
        return course_id

    def read_courses_email(self):
        cards = self.get_course_cards()

        if not cards:
            raise Exception("🟥 No encontré ningun curso")

        course_message: Dict[str, List[Message]] = {}

        for i in range(len(cards)):
            course_id = self.go_to_course(i)
            print("Leyendo mensajes de ", course_id)

            messages = self.read_email()
            course_message[course_id] = messages
            self.driver.go_to("/miscursos.php")

        return course_message

    def read_email(self):
        self.driver.check_error()

        email_button = self.driver.get_element(By.ID, "nav-mail-popover-container")
        email_button.click()

        mail_elements = self.driver.get_element(
            By.CLASS_NAME, "mail-navbar-menu"
        ).find_elements(By.TAG_NAME, "a")
        bandeja = mail_elements[0]

        unread = self.driver.get_element(By.TAG_NAME, "span", bandeja)
        if not unread:
            return []

        unread_amount = unread.text

        if not bool(unread_amount):
            return []

        bandeja.click()
        messages: List[Message] = []
        unread_mesage_divs = self.driver.get_elements(By.CLASS_NAME, "mail_unread", 0)

        for _ in range(len(unread_mesage_divs)):
            self.driver.get_element(By.CLASS_NAME, "mail_unread").click()
            mail_div = self.driver.get_element(By.CLASS_NAME, "mail_content")

            user_from = self.driver.get_element(By.CLASS_NAME, "user_from")
            date = self.driver.get_element(By.CLASS_NAME, "mail_date")

            images = self.driver.get_elements(By.TAG_NAME, "img", mail_div) or []

            messages.append(Message("text", f"{user_from.text} dijo el {date.text}"))

            for image in images:
                if "icon" in image.get_attribute("class"):
                    continue
                image_bytes = self.driver.get_image(image.get_attribute("src"))
                messages.append(Message("photo", "", image_bytes))
            messages.append(Message("text", "✉️✉️✉️\n\n" + mail_div.text))
            try:
                self.driver.get_element(By.CLASS_NAME, "mail_goback").click()
            except:
                self.driver.refresh()

        return messages

    def get_course_post_messages(self):
        course_messages = []
        aprendizaje_button = self.driver.get_element(By.ID, "gridsection-2")
        aprendizaje_button.click()
        unread_forums = self.driver.get_elements(By.CLASS_NAME, "unread")
        if not unread_forums:
            return []
        for forum in unread_forums:
            if forum.text == "":
                continue
            try:
                parent_div = forum.find_element(By.XPATH, "..").find_element(
                    By.XPATH, ".."
                )
                parent_div.find_element(By.CLASS_NAME, "isrestricted")
                continue
            except:
                pass
            messages: List[Message] = []
            forum.click()
            self.driver.check_error()
            # more than 1??
            concrete_forum = self.driver.get_element(By.CLASS_NAME, "hasunread")
            if not concrete_forum:
                raise
            first_link = self.driver.get_element(By.TAG_NAME, "a", concrete_forum)
            first_link.click()

            unread_posts = self.driver.get_elements(By.CLASS_NAME, "unread") or []

            for post in unread_posts:
                from_content = self.driver.get_element(By.CLASS_NAME, "mb-3", post)
                messages.append(Message("text", from_content.text))
                post_content_container = self.driver.get_element(
                    By.CLASS_NAME, "post-content-container", post
                )
                images = (
                    self.driver.get_elements(By.TAG_NAME, "img", post_content_container)
                    or []
                )
                for image in images:
                    # TODO: review duplication
                    image_bytes = self.driver.get_image(image.get_attribute("src"))
                    messages.append(Message("photo", "", image_bytes))

                messages.append(
                    Message("text", f"💬💬💬 {post_content_container.text}")
                )
                try:
                    ##more than 1??
                    attachments = post.parent.find_elements(
                        By.CLASS_NAME, "rspkr_dr_added"
                    )
                    for attachment in attachments:
                        bytes_file = self.driver.get_file(
                            attachment.get_attribute("href")
                        )
                        messages.append(
                            Message("file", attachment.text.strip(), bytes_file)
                        )
                except:
                    pass
                # browser.save_screenshot('...')
            course_messages.extend(messages)
        return course_messages

    def get_unreaded_posts(self):
        # TODO: send some code lines to the driver
        cards = self.get_course_cards()
        course_message: Dict[str, List[Message]] = {}
        for i in range(len(cards)):
            course_id = self.go_to_course(i)
            self.driver.check_error()
            course_message[course_id] = self.get_course_post_messages()
            self.driver.go_to("/miscursos.php")
        return course_message
