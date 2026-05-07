from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class WaitUtils:

    @staticmethod
    def wait_for_element(driver, locator, timeout=15):
        """Wait for element to be visible with increased timeout"""
        return WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    @staticmethod
    def wait_for_element_clickable(driver, locator, timeout=15):
        """Wait for element to be clickable"""
        return WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

    @staticmethod
    def wait_for_page_load(driver, timeout=20):
        """Wait for page to fully load"""
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

    @staticmethod
    def wait_for_element_with_retry(driver, locator, timeout=15, retries=2):
        """Wait for element with retry mechanism"""
        for attempt in range(retries + 1):
            try:
                return WaitUtils.wait_for_element(driver, locator, timeout)
            except TimeoutException:
                if attempt == retries:
                    raise
                driver.refresh()
                WaitUtils.wait_for_page_load(driver)

    @staticmethod
    def safe_click(driver, locator, timeout=15):
        """Safe click with proper waits"""
        element = WaitUtils.wait_for_element_clickable(driver, locator, timeout)
        element.click()