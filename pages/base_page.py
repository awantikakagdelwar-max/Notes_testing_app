from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:


    def __init__(self, driver):
        self.driver = driver

    def wait(self, locator, timeout=20):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )

    def type(self, locator, text):
        element = self.wait(locator)
        element.clear()
        element.send_keys(text)

    def click(self, locator):
        element = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(locator)
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", element)
        try:
            element.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", element)