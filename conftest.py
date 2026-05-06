import allure
import pytest
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException

from utils.screenshot import save_screenshot


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)
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
        driver.current_url

        report_dir = Path(item.config.rootpath)
        screenshot_path = save_screenshot(driver, item.name, report_dir)

        html_plugin = item.config.pluginmanager.getplugin("html")

        if html_plugin:
            extra = getattr(report, "extra", [])
            extra.append(html_plugin.extras.image(str(screenshot_path)))
            report.extra = extra

        with open(screenshot_path, "rb") as f:
            allure.attach(
                f.read(),
                name="failure_screenshot",
                attachment_type=allure.attachment_type.PNG
            )

    except WebDriverException:
        pass

    except Exception:
        pass