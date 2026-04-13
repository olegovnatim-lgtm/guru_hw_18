import pytest
import logging
import attach
import os
from dotenv import load_dotenv
from selene import browser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

logger = logging.getLogger(__name__)


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        default="chrome",
        help="Browser to use"
    )
    parser.addoption(
        "--browser_version",
        default="128.0",
        help="Browser version to use"
    )
    parser.addoption(
        "--headless",
        default="false",
        choices=("true", "false"),  # строки вместо булевых
        help="Run browser in headless mode"
    )
    parser.addoption(
        "--base-url",
        default="https://demoqa.com",
        help="URL for test"
    )
    parser.addoption(
        "--selenoid-url",
        default="selenoid.autotests.cloud/wd/hub",
        help="URL of Selenoid"
    )
    parser.addoption(
        "--window-size",
        default="1920,1080",
        choices=(
            "1920,1080",
            "1280,720",
            "768,1024",
        ),
        help="Window Size of Browser"
    )


@pytest.fixture(scope='function', autouse=True)
def setup_browser(request):
    login = os.getenv("SELENOID_LOGIN")
    password = os.getenv("SELENOID_PASSWORD")

    browser_name     = request.config.getoption("--browser")
    browser_version  = request.config.getoption("--browser_version")
    headless         = request.config.getoption("--headless")
    base_url         = request.config.getoption("--base-url")
    selenoid_url     = request.config.getoption("--selenoid-url")
    window_size      = request.config.getoption("--window-size")  # добавили

    options = Options()

    if headless:
        options.add_argument("--headless")

    options.add_argument(f"--window-size={window_size}")  # добавили

    selenoid_capabilities = {
        "browserName": browser_name,
        "browserVersion": browser_version,
        "selenoid:options": {
            "enableVNC": True,
            "enableVideo": True
        }
    }
    options.capabilities.update(selenoid_capabilities)

    driver = webdriver.Remote(
        command_executor = f"https://{login}:{password}@{selenoid_url}",
        options=options
    )

    browser.config.driver = driver
    browser.config.base_url = base_url

    yield browser

    attach.add_screenshot(driver)
    attach.add_page_source(driver)
    attach.add_console_logs(driver)
    attach.add_video(driver)

    driver.quit()


@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv()

@pytest.fixture(scope="session", autouse=True)
def log_options(request, load_env):
    logger.info("=== Параметры запуска ===")
    logger.info(f"browser:         {request.config.getoption('--browser')}")
    logger.info(f"browser_version: {request.config.getoption('--browser_version')}")
    logger.info(f"headless:        {request.config.getoption('--headless')}")
    logger.info(f"base_url:        {request.config.getoption('--base-url')}")
    logger.info(f"selenoid_url:    {request.config.getoption('--selenoid-url')}")
    logger.info(f"window_size:     {request.config.getoption('--window-size')}")
    logger.info(f"SELENOID_LOGIN:  {os.getenv('SELENOID_LOGIN')}")
    logger.info("========================")
