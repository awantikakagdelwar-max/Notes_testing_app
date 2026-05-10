import os
import allure
import pytest

from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException
from webdriver_manager.chrome import ChromeDriverManager

from utils.screenshot import save_screenshot


@pytest.fixture
def driver():

    remote_url = os.getenv(
        "SELENIUM_REMOTE_URL"
    )

    chrome_options = Options()

    # chrome_options.add_argument("--headless=new")

    chrome_options.add_argument("--no-sandbox")

    chrome_options.add_argument(
        "--disable-dev-shm-usage"
    )

    chrome_options.add_argument("--disable-gpu")

    chrome_options.add_argument(
        "--window-size=1920,1080"
    )

    chrome_options.add_argument(
        "--disable-extensions"
    )

    chrome_options.add_argument(
        "--disable-infobars"
    )

    if remote_url:
        driver = webdriver.Remote(
            command_executor=remote_url,
            options=chrome_options
        )
    else:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(
            service=service,
            options=chrome_options
        )

    driver.implicitly_wait(10)

    yield driver

    driver.quit()


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):

    outcome = yield

    report = outcome.get_result()

    if report.when != "call" or report.passed:
        return

    driver = item.funcargs.get("driver")

    if not driver:
        return

    try:

        report_dir = Path(item.config.rootpath)

        screenshot_path = save_screenshot(
            driver,
            item.name,
            report_dir
        )

        with open(screenshot_path, "rb") as f:

            allure.attach(
                f.read(),
                name="failure_screenshot",
                attachment_type=allure.attachment_type.PNG
            )

    except WebDriverException:
        pass