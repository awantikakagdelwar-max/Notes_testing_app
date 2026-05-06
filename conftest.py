import allure
import pytest
from pathlib import Path
from selenium.common.exceptions import WebDriverException

from fixtures.browser_fixture import driver
from utils.screenshot import save_screenshot


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):

    outcome = yield
    report = outcome.get_result()

    if report.when != "call" or report.passed:
        return

    driver = item.funcargs.get("driver")

    if driver is None:
        return

    try:
        # check browser still exists
        driver.current_window_handle

        report_dir = Path(item.config.rootpath)
        screenshot_path = save_screenshot(driver, item.name, report_dir)

        html_plugin = item.config.pluginmanager.getplugin("html")

        if html_plugin is not None:
            extra = getattr(report, "extra", [])
            extra.append(html_plugin.extras.image(str(screenshot_path)))
            report.extra = extra

        with open(screenshot_path, "rb") as image_file:
            allure.attach(
                image_file.read(),
                name="failure_screenshot",
                attachment_type=allure.attachment_type.PNG
            )

    except WebDriverException:
        # browser already closed
        pass

    except Exception:
        pass