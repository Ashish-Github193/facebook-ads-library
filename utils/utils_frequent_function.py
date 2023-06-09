import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By


def check_if_more_data_available(driver: webdriver.Chrome, total: int) -> bool:
    complete_page = driver.find_element(By.CLASS_NAME, "_8n_0")
    target_elements_xpath = "./div[2]/div[4]/div[1]/*"
    return total == len(complete_page.find_elements(By.XPATH, target_elements_xpath))


def get_inner_html_by_xpath(driver: webdriver.Chrome, xpath: str) -> BeautifulSoup:
    element = driver.find_element(By.XPATH, xpath)
    innerHTML = element.get_attribute("innerHTML")
    return BeautifulSoup(innerHTML, "html.parser")


def get_xpath_for_each_element(
    start: int, number_of_elements: int, xpath_head: str, xpath_tail=""
):
    for iter in range(start, start + number_of_elements + 1):
        yield f"{xpath_head}[{iter}]{xpath_tail}"


def filter_text(text):
    text = re.sub(r"<.*?>", "", text)
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)

    text = text.lower()
    text = re.sub(r"\s+", " ", text)

    stopwords = ["the", "and", "is", "in", "it", "of", "to", "that", "this", "for"]
    text = " ".join(word for word in text.split() if word not in stopwords)
    return text
