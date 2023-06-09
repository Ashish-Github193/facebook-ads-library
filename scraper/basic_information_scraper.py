import logging
from multiprocessing.util import info
from bs4 import BeautifulSoup
from selenium import webdriver
from contextlib import suppress

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from utils.utils_frequent_function import filter_text, get_inner_html_by_xpath


def get_advertiser_texts(info_block: BeautifulSoup):
    elements = info_block.find_all(text=True)
    return [e.get_text() for e in elements]


def extract_advertiser_info(item: list):
    print(item)
    try:
        name = item[0]
    except:
        return None

    try:
        advertiser_type = item[1]
    except Exception:
        advertiser_type = "-"

    try:
        description = item[2]
        if (
            "//" in description
            or "//" not in description
            and len(filter_text(description)) == 0
        ):
            description = "-"
    except Exception:
        description = "-"

    try:
        website = next(
            (e.strip() for e in item if (isinstance(e, str) and e.startswith("http"))),
            None,
        )
        if website is None:
            return None
    except Exception:
        return None

    return {
        "Name": name,
        "Type": advertiser_type,
        "Description": description,
        "Website": website,
    }


def hover_element_if_exists(
    driver: webdriver.Chrome, element: WebElement, info_block_constructor_xpath: str
):
    actions = ActionChains(driver)
    actions.move_to_element(element)
    actions.perform()

    relative_xpath = "/div/div[1]/div[1]/div/div/div[1]/div[2]"
    element = driver.find_element(
        By.XPATH, info_block_constructor_xpath + relative_xpath
    )
    return get_inner_html_by_xpath(
        driver=driver, xpath=info_block_constructor_xpath + relative_xpath
    )


def hover_element(driver: webdriver.Chrome, element: WebElement, xpath: str):
    info_block_constructor_xpath = f"{xpath}/div/div[3]/div/div/div[3]/div"
    try:
        return hover_element_if_exists(driver, element, info_block_constructor_xpath)
    except Exception:
        return None


def find_advertiser_name_element_xpath(
    parent_element: WebElement, parent_element_xpath: str
):
    with suppress(Exception):
        for a_tag in parent_element.find_elements(By.TAG_NAME, "a"):
            href = a_tag.get_attribute("href")
            if href and href.startswith("https://facebook.com/"):
                return f"{parent_element_xpath}//a[@href='{href}']"

    return None


def get_advertiser_information_with_information_block(
    driver: webdriver.Chrome, parent_element: WebElement, advertisement_xpath: str
):
    element_xpath = find_advertiser_name_element_xpath(
        parent_element=parent_element, parent_element_xpath=advertisement_xpath
    )

    with suppress(Exception):
        element = driver.find_element(By.XPATH, element_xpath)
        return hover_element(driver=driver, element=element, xpath=advertisement_xpath)  # type: ignore

    logging.warning(
        f"Message: No ELEMENT found to hover on | Scraper: Basic information scraper | Function: get_advertiser_information_with_information_block | More info: xpath: {element_xpath}"
    )
    return None


def scrape_basic_information(
    driver: webdriver.Chrome, parent_element: WebElement, advertisement_xpath: str
):
    html = get_advertiser_information_with_information_block(
        driver=driver,
        parent_element=parent_element,
        advertisement_xpath=advertisement_xpath,
    )

    if html is not None:
        get_advertiser_text_list = get_advertiser_texts(info_block=html)
        advertiser_information = extract_advertiser_info(get_advertiser_text_list)  # type: ignore

        return advertiser_information

    logging.warning(
        "Message: No HTML found | Scraper: Basic information scraper | Function: scrape basic information"
    )
    logging.warning(f"#{'-'*30}#")
    return None
