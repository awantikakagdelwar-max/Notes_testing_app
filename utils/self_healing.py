from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

class SelfHealingElement:

    @staticmethod
    def find_element(driver, locators):

        for locator in locators:
            try:
                by, value = locator
                return driver.find_element(by, value)

            except NoSuchElementException:
                continue

        raise NoSuchElementException("Element not found with any locator")