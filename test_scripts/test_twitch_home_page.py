import pytest

from page_objects.main_page import MainPage


class TestTwitchMainPage:

    @pytest.mark.positive
    @pytest.mark.regression
    def test_open_stream(self, driver):
        main_page = MainPage(driver)

        # go to twitch
        main_page.open()
        main_page.log.info("Opening Twitch main page")
        main_page.close_page_modal()
        main_page.log.info("Closing page modal if visible")
        assert main_page.is_browse_button_displayed(), "Browse button is not displayed"
        main_page.log.info("Browse button displayed")

        # click in the search icon and input StarCraft II
        main_page.find_stream("StarCraft II")
        main_page.log.info("Browsing StarCraft II and entering the category")
        assert main_page.expected_starcraft_search_url in driver.current_url, "Actual URL is not the StarCraft II category"
        main_page.log.info("StarCraft II category found")

        # scroll down twice
        main_page.scroll_down_twice()
        main_page.log.info("Scrolling down twice")

        # select one streamer
        main_page.enter_stream()
        main_page.log.info("Entering stream")
        assert main_page.wait_stream_to_load(), "Stream did not load properly"
        main_page.take_screenshot()
        main_page.log.info("Stream loaded successfully and screenshot taken")
