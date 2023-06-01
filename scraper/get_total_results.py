
from selenium                      import webdriver
from utils.utils_frequent_function import get_inner_html_by_xpath


def get_total_found_results (driver: webdriver.Chrome):
    xpath = "/html/body/div[1]/div[1]/div[1]/div/div/div/div[5]/div[1]/div/div/div/div/div/div[1]/div"
    result = get_inner_html_by_xpath(driver=driver, xpath=xpath).get_text()
    result = int(''.join(filter(str.isdigit, result)))
    return result