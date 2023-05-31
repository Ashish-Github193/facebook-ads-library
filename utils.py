import re
import csv
import codecs
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager


############################################################################################################
########################################## Frequent function ###############################################
############################################################################################################
def initialize_chrome() -> webdriver.Chrome:
    chrome_options = Options()
    chrome_options.add_argument('--incognito')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument('--blink-settings=imagesEnabled=false')
    return webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)


def get_inner_html_by_xpath(driver: webdriver.Chrome, xpath: str) -> BeautifulSoup:
    element = driver.find_element(By.XPATH, xpath)
    innerHTML = element.get_attribute("innerHTML")
    return BeautifulSoup(innerHTML, "html.parser")


def get_xpath_for_each_element(
    xpath_head: str, xpath_tail: str, start: int, number_of_elements: int
):
    for iter in range(start, start + number_of_elements + 1):
        yield f"{xpath_head}[{iter}]{xpath_tail}"


############################################################################################################
########################################## Scrapping util function #########################################
############################################################################################################
def hover_element(
    driver: webdriver.Chrome, element: WebElement, xpath: str, xpath_tail: str
):
    if element is None: return None
    info_block_constructor_xpath = (
        f"{xpath[:-len(xpath_tail)]}/div/div[3]/div/div/div[3]/div"
    )
    try:
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()
        return get_inner_html_by_xpath(
            driver=driver, xpath=info_block_constructor_xpath
        )
    except Exception:
        print("element not found", "| xpath:", info_block_constructor_xpath)


def get_advertiser_info_block(
    driver: webdriver.Chrome, index: int, number_of_elements: int
) -> BeautifulSoup:  # type: ignore
    xpath_head = "/html/body/div[1]/div[1]/div[1]/div/div/div/div[5]/div[2]/div[2]/div[4]/div[1]/div"
    xpath_tail = "/div/div[3]/div/div/div[1]"

    for xpath in get_xpath_for_each_element(
        xpath_head=xpath_head,
        xpath_tail=xpath_tail,
        start=index,
        number_of_elements=number_of_elements,
    ):
        hover_path = f"{xpath[:-len(xpath_tail)]}/div/div[3]/div/div/div[1]/div/div/div/div/div[1]/div"
        element = None

        try:
            element = driver.find_element(By.XPATH, hover_path)
        except Exception:
            try:
                element = driver.find_element(By.XPATH, f"{hover_path}/div")
            except Exception:
                try:
                    element = driver.find_element(By.XPATH, f"{hover_path}/a")
                except Exception:
                    yield None

        yield hover_element(driver=driver, element=element, xpath=xpath, xpath_tail=xpath_tail)  # type: ignore


def get_advertiser_texts(info_block: BeautifulSoup):  # type: ignore
    elements = info_block.find_all(text=True)
    return [e.get_text() for e in elements]



############################################################################################################
########################################## Scrapping function ##############################################
############################################################################################################
def get_total_results (driver: webdriver.Chrome):
    xpath = "/html/body/div[1]/div[1]/div[1]/div/div/div/div[5]/div[1]/div/div/div/div/div/div[1]/div"
    result = get_inner_html_by_xpath(driver=driver, xpath=xpath).get_text()
    result = int(''.join(filter(str.isdigit, result)))
    return result


def get_advertisers_names(driver, index: int, number_of_elements: int):
    xpath_head = "/html/body/div[1]/div[1]/div[1]/div/div/div/div[5]/div[2]/div[2]/div[4]/div[1]/div"
    xpath_tail = "/div/div[3]/div/div/div[1]"

    for xpath in get_xpath_for_each_element(
        xpath_head=xpath_head,
        xpath_tail=xpath_tail,
        start=index,
        number_of_elements=number_of_elements,
    ):
        try:
            element_ = get_inner_html_by_xpath(driver=driver, xpath=xpath)
            yield element_.get_text()[:-9]
        except Exception:
            continue


def extract_company_info(item: list):
    
    # name of advertiser
    try: name = item[0]
    except: return None

    # description of advertiser
    description = max(item, key=len)
    if ( "//" in description or "//" not in description and len(filter_text(description)) == 0 ):
        description = "-"

    # website url of advertiser
    website = next( (e.strip() for e in item if (isinstance(e, str) and e.startswith("http"))), None,)

    if website is None: return None # type: ignore

    return {"name": name, "description": description, "website": website}


############################################################################################################
########################################## Scrapping function ##############################################
############################################################################################################
def check_if_more_data_available(driver: webdriver.Chrome, end: int) -> bool:
    try:
        element_xpath = f"//*[@id='content']/div/div/div/div[5]/div[2]/div[2]/div[4]/div[1]/div[{end+1}]"
        get_inner_html_by_xpath(driver=driver, xpath=element_xpath)
        return True
    except Exception:
        return False


############################################################################################################
########################################## Text filtering function #########################################
############################################################################################################
def filter_text(text):
    text = re.sub(r"<.*?>", "", text)
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)

    text = text.lower()
    text = re.sub(r"\s+", " ", text)

    stopwords = ["the", "and", "is", "in", "it", "of", "to", "that", "this", "for"]
    text = " ".join(word for word in text.split() if word not in stopwords)
    return text


############################################################################################################
########################################## Root scraping function ##########################################
############################################################################################################
def scrape_data(driver, index: int, number_of_elements: int):
    for info_block_text_list in get_advertiser_info_block(driver=driver, index=index, number_of_elements=number_of_elements):

        # Skip to the next iteration if info_block is None
        if info_block_text_list is None: continue
        
        # Extract company information from the info_block
        get_advertiser_text_list = get_advertiser_texts(info_block=info_block_text_list) # type: ignore
        company_info = extract_company_info(get_advertiser_text_list)

        # Skip to the next iteration if company_info is None
        if company_info is None: continue

        # Yield the extracted data
        yield company_info


############################################################################################################
########################################## write in csv function ###########################################
############################################################################################################
def write_list_of_dicts_to_csv(headers, data_list, filename):
    with codecs.open(filename, 'a', encoding='utf-8', errors='replace') as file:
        writer = csv.DictWriter(file, fieldnames=headers)

        # Check if the file is empty
        if file.tell() == 0:
            writer.writeheader()

        # write data in separate rows
        writer.writerows(data_list)

    # print in console that 'Data is successfully appended in the csv file'
    print(f'Data appended to {filename} successfully.')