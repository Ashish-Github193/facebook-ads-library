from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

def check_if_more_data_available(driver: webdriver.Chrome, end: int) -> bool:
    try:
        element_xpath = f"//*[@id='content']/div/div/div/div[5]/div[2]/div[2]/div[4]/div[1]/div[{end+1}]"
        get_inner_html_by_xpath(driver=driver, xpath=element_xpath)
        return True
    except Exception:
        return False


def get_inner_html_by_xpath(driver: webdriver.Chrome, xpath: str) -> BeautifulSoup:
    element = driver.find_element(By.XPATH, xpath)
    innerHTML = element.get_attribute("innerHTML")
    return BeautifulSoup(innerHTML, "html.parser")


def get_xpath_for_each_element( start: int, number_of_elements: int, xpath_head: str, xpath_tail="" ):
    for iter in range(start, start + number_of_elements + 1):
        yield f"{xpath_head}[{iter}]{xpath_tail}"