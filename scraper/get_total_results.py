
from selenium                      import webdriver
from selenium.webdriver.common.by  import By
from utils.utils_frequent_function import get_inner_html_by_xpath


def get_total_found_results (driver: webdriver.Chrome):
    xpath = "/html/body/div[1]/div[1]/div[1]/div/div/div/div[5]/div[1]/div/div/div/div/div/div[1]/div"
    result = get_inner_html_by_xpath(driver=driver, xpath=xpath).get_text()
    result = int(''.join(filter(str.isdigit, result)))
    return result


def total_advertisement_on_current_page (driver: webdriver.Chrome):
    complete_page = driver.find_element(By.CLASS_NAME, "_8n_0")
    target_elements_xpath = "./div[2]/div[4]/div[1]/*"
    return len(complete_page.find_elements(By.XPATH, target_elements_xpath))