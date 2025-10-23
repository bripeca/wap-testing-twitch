from selenium.common import ElementClickInterceptedException, TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from page_objects.base_page import BasePage
from utilities.logger import get_logger


class MainPage(BasePage):
    # main page url
    main_page_url = "https://m.twitch.tv"
    starcraft_category_url = "https://m.twitch.tv/directory/category/starcraft-ii"

    # locators for twitch main page
    browse_button = (By.XPATH, "//a[.//div[text()='Browse']]")
    browse_field = (By.XPATH, "//input[@placeholder='Search']")
    starcraft_search_result = (By.XPATH, "//a[@href='/directory/category/starcraft-ii']//img")
    first_displayed_stream = (By.XPATH, "//div[@role='list']//article[1]//button[contains(@class,'tw-link')]")
    content_modal_watch_button = (By.XPATH, "//button[@data-a-target='content-classification-gate-overlay-start-"
                                            "watching-button']")
    follow_button = (By.XPATH, "//button[contains(., 'Follow')]")

    # driver initialization
    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        self.log = get_logger(self.__class__.__name__)

    def open(self):
        super().open_url(self.main_page_url)

    @property
    def expected_starcraft_search_url(self) -> str:
        return self.starcraft_category_url

    # search for input and click on the Starcraft II category
    def find_stream(self, search_input: str):
        super().click(self.browse_button)
        super().type(self.browse_field, search_input)
        super().click(self.starcraft_search_result)

    # double scroll down twice, if needed only one it can be called from the base_page.py
    def scroll_down_twice(self):
        super().scroll_down()
        super().scroll_down()

    def enter_stream(self):
        super().click(self.first_displayed_stream)
        # this will look for the content gate modal if enabled on a stream
        # if not found it will not block test scrips and will continue as normal
        buttons = self.driver.find_elements(*self.content_modal_watch_button)
        if not buttons:
            return  # modal not present — continue test normally
        try:
            buttons[0].click()
        # if button is not visible for any reason it will click the button anyways
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", buttons[0])

    def is_browse_button_displayed(self) -> bool:
        return super().is_displayed(self.browse_button)

    # check constantly if the stream loads in the page.
    def wait_stream_to_load(self) -> bool:
        try:
            super().wait_until_element_is_visible(self.follow_button, 10)
            return True
        except TimeoutException:
            return False

    '''
    using the following test function to close any modal overlays in the mobile version of the page, there are currently
    2 different modals with different elements, this function will click out of the modal independently of which of the
    different modals appear and will not affect the test if none of the modals appears.
    '''

    def close_page_modal(self):
        actions = ActionChains(self.driver)
        actions.move_by_offset(0, 0).click().perform()
