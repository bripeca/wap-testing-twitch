from selenium.common import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

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
    content_modal_watch_button = (By.XPATH,
                                  "//button[@data-a-target='content-classification-gate-overlay-start-""watching-button']")
    follow_button = (By.XPATH, "//button[contains(., 'Follow')]")

    # driver initialization
    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        self.log = get_logger(self.__class__.__name__)

    def open(self):
        super().open_url(self.main_page_url)
        self.log.info("Opening Twitch main page")

    @property
    def expected_starcraft_search_url(self) -> str:
        return self.starcraft_category_url

    # search for input and click on the Starcraft II category
    def find_stream(self, search_input: str):
        self.log.info("Finding game category")
        super().click(self.browse_button)
        super().type(self.browse_field, search_input)
        super().click(self.starcraft_search_result)

    # scroll up twice, modify the times variable to make it once or more than twice.
    def scroll_up_twice(self):
        self.log.info("Scrolling down twice")
        super().scroll_up(times=2)

    # scroll down twice, modify the times variable to make it once or more than twice.
    def scroll_down_twice(self):
        self.log.info("Scrolling up twice")
        super().scroll_down(times=2)

    def enter_stream(self):
        self.log.info("Entering stream")
        super().click(self.first_displayed_stream)

    def is_browse_button_displayed(self) -> bool:
        self.log.info("Looking for browse button")
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
        self.log.info("Closing page modal if visible")
        actions = ActionChains(self.driver)
        actions.move_by_offset(0, 0).click().perform()

    # close the "intended for certain audiences" modal when opening some streams, if found, if not it ignores it.
    def close_content_modal(self, timer: int = 5):
        self.log.info("Closing content modal if visible")
        try:
            wait = WebDriverWait(self.driver, timer)
            wait.until(EC.element_to_be_clickable(self.content_modal_watch_button)).click()
        except TimeoutException:
            pass
