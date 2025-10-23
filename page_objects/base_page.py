import time

from selenium.common import NoSuchElementException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from utilities.logger import get_logger


class BasePage:

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.log = get_logger(self.__class__.__name__)

    def open_url(self, url: str):
        self.driver.get(url)

    def find(self, locator: tuple) -> WebElement:
        return self.driver.find_element(*locator)

    def type(self, locator: tuple, text: str, timer: int = 5):
        self.wait_until_element_is_visible(locator, timer)
        self.find(locator).send_keys(text)

    def click(self, locator: tuple, timer: int = 5):
        self.wait_until_element_is_visible(locator, timer)
        self.find(locator).click()

    def wait_until_element_is_visible(self, locator: tuple, timer: int = 10):
        wait = WebDriverWait(self.driver, timer)
        wait.until(ec.visibility_of_element_located(locator))

    def is_displayed(self, locator: tuple) -> bool:
        try:
            return self.find(locator).is_displayed()
        except NoSuchElementException:
            return False

    # a couple of waits to make sure the scroll is smooth and won't break the test
    def scroll_down(self):
        time.sleep(1)
        self.driver.execute_script("window.scrollBy(0, 750);")
        time.sleep(1)

    def current_url(self) -> str:
        return self.driver.current_url

    def take_screenshot(self, name: str = "screenshot"):
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        file_path = f"test_scripts/screenshots/{name}_{timestamp}.png"
        self.driver.save_screenshot(file_path)
        print("Screenshot saved: {file_path}")
        return file_path
