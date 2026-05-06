from datetime import datetime
from pathlib import Path


def screenshot_dir(root_path: Path) -> Path:
    path = root_path / "screenshots"
    path.mkdir(parents=True, exist_ok=True)
    return path


def sanitize_filename(name: str) -> str:
    allowed = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._- ")
    return "".join(c if c in allowed else "_" for c in name).strip().replace(" ", "_")


def save_screenshot(driver, test_name: str, root_path: Path | None = None) -> Path:
    if root_path is None:
        root_path = Path.cwd()

    directory = screenshot_dir(root_path)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"{sanitize_filename(test_name)}_{timestamp}.png"
    screenshot_path = directory / file_name
    driver.save_screenshot(str(screenshot_path))
    return screenshot_path
