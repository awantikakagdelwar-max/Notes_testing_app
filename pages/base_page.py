from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:

    def __init__(self, driver):

        self.driver = driver

        self.wait = WebDriverWait(driver, 30)

    def click(self, locator):

        element = self.wait.until(
            EC.element_to_be_clickable(locator)
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            element
        )

        try:
            element.click()

        except Exception:

            self.driver.execute_script(
                "arguments[0].click();",
                element
            )

    def type(self, locator, value):

        element = self.wait.until(
            EC.visibility_of_element_located(locator)
        )

        element.clear()

        element.send_keys(value)

    def get_text(self, locator):

        element = self.wait.until(
            EC.visibility_of_element_located(locator)
        )

        return element.text
    
    def get_element(self, locator):

        return self.wait.until(
            EC.visibility_of_element_located(locator)
        )