from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from pages.base_page import BasePage

class ProductPage(BasePage):

    ADD_NOTE = (By.CSS_SELECTOR, "button[data-testid='add-new-note']")
    TITLE = (By.ID, "title")
    DESCRIPTION = (By.ID, "description")
    SAVE = (By.CSS_SELECTOR, "button[data-testid='note-submit']")
    NOTES = (By.CSS_SELECTOR, "div[data-testid='note-card']")
    NOTE_TITLE = (By.CSS_SELECTOR, "div[data-testid='note-card-title']")
    NOTE_DELETE = (By.CSS_SELECTOR, "button[data-testid='note-delete']")
    DELETE_CONFIRM = (By.CSS_SELECTOR, "button[data-testid='note-delete-confirm']")

    def create_note(self, title, desc):
        self.click(self.ADD_NOTE)
        self.type(self.TITLE, title)
        self.type(self.DESCRIPTION, desc)
        self.click(self.SAVE)

    def get_all_notes(self):
        return self.driver.find_elements(*self.NOTES)

    def note_card_locator_for_title(self, title):
        escaped_title = title.replace('"', '\\"')
        return (
            By.XPATH,
            f"//div[@data-testid='note-card'][.//div[@data-testid='note-card-title' and normalize-space()=\"{escaped_title}\"]]"
        )

    def wait_for_note_presence(self, title, timeout=20):
        locator = self.note_card_locator_for_title(title)
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )

    def wait_for_note_absence(self, title, timeout=20):
        locator = self.note_card_locator_for_title(title)

        def element_absent(driver):
            try:
                elems = driver.find_elements(*locator)
                return len(elems) == 0 or all(not elem.is_displayed() for elem in elems)
            except Exception:
                return True

        return WebDriverWait(self.driver, timeout).until(element_absent)

    def delete_note_by_index(self, index=0):
        notes = self.get_all_notes()
        if len(notes) <= index:
            raise IndexError("No note found at index {}".format(index))

        delete_btn = notes[index].find_element(*self.NOTE_DELETE)
        self.driver.execute_script("arguments[0].click();", delete_btn)
        self.wait(self.DELETE_CONFIRM)
        self.click(self.DELETE_CONFIRM)

    def delete_note_by_title(self, title):
        locator = self.note_card_locator_for_title(title)
        note_card = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located(locator)
        )
        delete_btn = note_card.find_element(*self.NOTE_DELETE)
        self.driver.execute_script("arguments[0].click();", delete_btn)
        self.wait(self.DELETE_CONFIRM)
        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(self.DELETE_CONFIRM)
        )
        self.click(self.DELETE_CONFIRM)
        self.wait_for_note_absence(title, timeout=30)

    def delete_first_note(self):
        self.delete_note_by_index(0)
