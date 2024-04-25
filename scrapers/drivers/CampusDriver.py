import json
import logging
import time

import requests
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

from constants import COOKIES


logger = logging.getLogger(__name__)
CAMPUS_URL = "https://campus0d.unad.edu.co/campus"


class CampusDriver:

    def __init__(self):
        self.tabs = {}
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        # Unknown options
        # chrome_options.add_argument("--enable-features=AllowGeolocationOnInsecureOrigins")
        # chrome_options.add_argument("--disable-features=BlockNonSecureSubresources")
        # chrome_options.add_argument("--disable-features=BlockInsecurePrivateNetworkRequests")
        # chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.geolocation": 0})
        # chrome_options.add_argument("--use-fake-ui-for-media-stream")
        # chrome_options.add_argument("--use-fake-device-for-media-stream")
        # chrome_options.add_argument("--disable-web-security")
        # chrome_options.add_argument("--disable-gpu")  # Deshabilitar la GPU
        # chrome_options.add_argument("--window-size=1920x1080")
        # chrome_options.add_argument("--allow-running-insecure-content")
        self.driver = webdriver.Chrome(options=chrome_options)
        logger.info("Chrome driver started")

    def add_cookies(self):
        for cookie in COOKIES:
            self.driver.add_cookie(cookie)

    def refresh(self):
        self.driver.refresh()

    def check_geolocation(self):
        # close permissions alert
        try:
            print("... cerrando alert")
            alert = self.driver.switch_to.alert
            alert.accept()
            print("ejecutando js")
            self.driver.execute_script(
                """ 
                    window.navigator.geolocation.getCurrentPosition = function(success) {
                    var position = {
                        "coords": {
                        "latitude": "555",
                        "longitude": "999"
                        }
                    };
                    success(position);
                    }
                    try{
                        localizar()
                    }catch{
                        console.log("nada")
                    }
                    """
            )
            # prints to review if the body is the expected
            print(self.driver.find_element(By.TAG_NAME, "body").text)
        except:
            print("No aparecio el alert de permisos")
            # print(self.driver.find_element(By.TAG_NAME, 'body').text)

    def retry_cookies(self):
        for i in range(10):
            failed_div = self.get_element(By.CLASS_NAME, "Cuerpo600")
            if (
                failed_div
                and failed_div.text
                == "Acceder a Campus Virtual\nSu navegador no logro procesar las cookies para el sitio unad.edu.co"
            ):
                print(f"retriying due to cookies: {i}")
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
        user_field = self.get_element(By.ID, "txtuser")
        user_field.send_keys("1022322066")
        button = self.driver.find_element(By.ID, "cmdIngresa2")
        button.click()

        pass_field = self.driver.find_element(By.ID, "txtclave2")
        pass_field.send_keys("!sTSjFWT43Wc_Ki")

        button = self.driver.find_element(By.ID, "cmdIngresa2")
        button.click()

        self.check_geolocation()

        print("Login succesful")

        self.driver.get("https://campus0d.unad.edu.co/campus/miscursos.php")
        self.check_geolocation()
        COOKIES += self.driver.get_cookies()
        with open("cookies.txt", "w") as file:
            file.write(json.dumps(COOKIES))

    def go_to_campus(self):
        self.driver.get(CAMPUS_URL)
        self.add_cookies()
        self.driver.get(CAMPUS_URL + "/accesit.php")
        if "accesit.php" not in self.driver.current_url:
            self.login()

    def get_elements(self, by, value, of=None):
        parent = self.driver
        if of:
            parent = of

        try:
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.presence_of_element_located((by, value)))
            return parent.find_elements(by, value)
        except:
            return

    def get_element(self, by, value, of=None):
        try:
            return self.get_elements(by, value, of)[0]
        except:
            return None

    def go_to(self, path):
        if self.tabs.get(path):
            target_tab = self.tabs.get(path)
            if target_tab != self.driver.current_window_handle:
                self.driver.close()
            self.driver.switch_to.window(target_tab)
            return

        self.driver.get(CAMPUS_URL + path)
        self.tabs[path] = self.driver.current_window_handle

    def go_to_last_tab(self):
        self.driver.switch_to.window(self.driver.window_handles[-1])

    def get_image(self, url: str):
        return requests.get(
            url, cookies={i["name"]: i["value"] for i in self.driver.get_cookies()}
        ).content

    def get_file(self, url: str):
        return requests.get(
            url, cookies={i["name"]: i["value"] for i in self.driver.get_cookies()}
        ).content

    def check_error(self):
        try:
            self.driver.driver.find_element(By.CLASS_NAME, "closebutton").click()
        except:
            pass
