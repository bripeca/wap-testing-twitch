import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture
def driver():
    # create mobile driver with the defined parameters below also providing a message on the console
    print(f"Creating driver")
    chrome_options = Options()
    mobile_settings = {"deviceName": "Pixel 7"}
    chrome_options.add_experimental_option('mobileEmulation', mobile_settings)

    # initialize webdriver
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

    # close the browser while also providing a message on the console
    yield driver
    print(f"Closing driver")
    driver.quit()
