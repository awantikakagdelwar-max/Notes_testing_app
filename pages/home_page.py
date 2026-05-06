from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class HomePage(BasePage):

    LOGOUT_BTN = (By.XPATH, "//button[text()='Logout']")

    def is_home_loaded(self):
        return self.wait(self.LOGOUT_BTN).is_displayed()