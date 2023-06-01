import contextlib
from selenium import webdriver
from selenium.webdriver.remote.webelement    import WebElement
from selenium.webdriver.common.action_chains import ActionChains

from utils.utils_frequent_function   import *
from utils.utils_frequent_function   import get_inner_html_by_xpath

def hover_element_if_exists (driver: webdriver.Chrome, element: WebElement, info_block_constructor_xpath: str):
    actions = ActionChains(driver)
    actions.move_to_element(element)
    actions.perform()

    return get_inner_html_by_xpath( driver=driver, xpath=info_block_constructor_xpath )


def hover_element( driver: webdriver.Chrome, element: WebElement, xpath: str ):    

    info_block_constructor_xpath = f"{xpath}/div/div[3]/div/div/div[3]/div"
    try: return hover_element_if_exists( driver, element, info_block_constructor_xpath )
    except Exception: return None


def find_advertiser_name_element_xpath(parent_element: WebElement, parent_element_xpath: str):

    with contextlib.suppress(Exception):
        for a_tag in parent_element.find_elements(By.TAG_NAME, "a"):
            href = a_tag.get_attribute("href")
            if href and href.startswith("https://facebook.com/"):
                return f"{parent_element_xpath}//a[@href='{href}']"

    return None

def get_advertiser_information_with_information_block (driver: webdriver.Chrome,
                                                       parent_element: WebElement,
                                                       advertisement_block_xpath: str):

    element_xpath = find_advertiser_name_element_xpath (parent_element=parent_element,
                                                        parent_element_xpath=advertisement_block_xpath)

    if advertisement_block_xpath is not None:
        try:
            element = driver.find_element(By.XPATH, element_xpath)
            return hover_element(driver=driver, element=element, xpath=advertisement_block_xpath)  # type: ignore
        except Exception: return None

    return None