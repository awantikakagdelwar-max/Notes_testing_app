from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage

class HomePage(BasePage):

    LOGOUT_BTN = (By.XPATH, "//button[text()='Logout']")

    def is_home_loaded(self):
        element = self.wait.until(EC.visibility_of_element_located(self.LOGOUT_BTN))
        return element.is_displayed()