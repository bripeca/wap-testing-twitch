import pytest

from page_objects.main_page import MainPage


class TestTwitchMainPage:

    @pytest.mark.positive
    @pytest.mark.regression
    def test_open_stream(self, driver):
        main_page = MainPage(driver)

        # go to twitch
        main_page.open()
        main_page.close_page_modal()
        assert main_page.is_browse_button_displayed(), "Browse button is not displayed"

        # click in the search icon and input StarCraft II
        main_page.find_stream("StarCraft II")
        assert main_page.expected_starcraft_search_url in driver.current_url, "Actual URL is not the StarCraft II category"

        # scroll down and up twice to find the first stream
        main_page.scroll_down_twice()
        main_page.scroll_up_twice()

        # select one streamer
        main_page.enter_stream()
        main_page.close_page_modal()
        main_page.close_content_modal()
        assert main_page.wait_stream_to_load(), "Stream did not load properly"
        main_page.take_screenshot()
        main_page.log.info("Stream loaded successfully and screenshot taken")
