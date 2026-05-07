import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage

class LoginPage(BasePage):

    EMAIL = (By.CSS_SELECTOR, "[data-testid='login-email']")
    PASSWORD = (By.CSS_SELECTOR, "[data-testid='login-password']")
    LOGIN_BTN = (By.CSS_SELECTOR, "[data-testid='login-submit']")

    def login(self, email, password):
        if '/login' not in self.driver.current_url:
            login_url = self.driver.current_url.rstrip('/') + '/login'
            self.driver.get(login_url)
            WebDriverWait(self.driver, 15).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
        self.type(self.EMAIL, email)
        self.type(self.PASSWORD, password)
        self.click(self.LOGIN_BTN)
        time.sleep(2)