from selenium import webdriver
from selenium.webdriver.common.by import By
from utils.utils_frequent_function import get_inner_html_by_xpath


def total_advertisement_on_current_page(driver: webdriver.Chrome):
    try:
        complete_page = driver.find_element(By.CLASS_NAME, "_8n_0")
        target_elements_xpath = "./div[2]/div[4]/div[1]/*"
    except Exception:
        print(
            "Element which is expected to have the total advertisement count, not found."
        )
        return 0
    return len(complete_page.find_elements(By.XPATH, target_elements_xpath))
