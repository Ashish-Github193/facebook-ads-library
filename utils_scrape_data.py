from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from scraper.basic_information_scraper import scrape_basic_information
from scraper.platform_names_scraper import get_advertising_platforms

from utils.utils_frequent_function import *
from utils.utils_initialise_function import *
from utils.utils_extras import merge_dictionaries


def group_scraped_data(driver: webdriver.Chrome, index: int, number_of_elements: int) -> BeautifulSoup:  # type: ignore
    xpath_head = "//div[contains(@class, '_8n_0')]/div[2]/div[4]/div[1]/div"
    for advertisement_xpath in get_xpath_for_each_element(
        xpath_head=xpath_head, start=index, number_of_elements=number_of_elements
    ):
        try:
            parent_element = driver.find_element(By.XPATH, advertisement_xpath)
        except Exception:
            yield [None, None] # type: ignore

        advertiser_basic_information = scrape_basic_information(
            driver=driver,
            parent_element=parent_element,
            advertisement_xpath=advertisement_xpath,
        )

        # if advertiser information found then get advertising platforms
        advertising_platform_names = None
        if advertiser_basic_information is not None:
            advertising_platform_names = get_advertising_platforms(
                parent_element=parent_element
            )

        yield [advertiser_basic_information, advertising_platform_names]


############################################################################################################
########################################## Root scraping function ##########################################
############################################################################################################
def scrape_data(driver, index: int, number_of_elements: int):
    for scraped_data in group_scraped_data(
        driver=driver, index=index, number_of_elements=number_of_elements
    ):
        if None not in scraped_data:
            yield merge_dictionaries(scraped_data)

        yield None