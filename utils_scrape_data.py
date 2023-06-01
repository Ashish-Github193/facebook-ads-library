import re, codecs, csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

from utils.utils_frequent_function   import *
from utils.utils_initialise_function import *
from utils.utils_scraping_function   import *

############################################################################################################
########################################## Scrapping util function ##############################################
############################################################################################################
def filter_text(text):
    text = re.sub(r"<.*?>", "", text)
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)

    text = text.lower()
    text = re.sub(r"\s+", " ", text)

    stopwords = ["the", "and", "is", "in", "it", "of", "to", "that", "this", "for"]
    text = " ".join(word for word in text.split() if word not in stopwords)
    return text


def write_list_of_dicts_to_csv(headers, data_list, filename):
    with codecs.open(filename, 'a', encoding='utf-8', errors='replace') as file:
        writer = csv.DictWriter(file, fieldnames=headers)

        # Check if the file is empty else write row
        if file.tell() == 0: writer.writeheader()
        writer.writerows(data_list)
    
    print(f'Data appended to {filename} successfully.')


############################################################################################################
########################################## Scrapping function ##############################################
############################################################################################################
def get_total_results (driver: webdriver.Chrome):
    xpath = "/html/body/div[1]/div[1]/div[1]/div/div/div/div[5]/div[1]/div/div/div/div/div/div[1]/div"
    result = get_inner_html_by_xpath(driver=driver, xpath=xpath).get_text()
    result = int(''.join(filter(str.isdigit, result)))
    return result


def get_advertiser_texts(info_block: BeautifulSoup):
    elements = info_block.find_all(text=True)
    return [e.get_text() for e in elements]


def extract_company_info(item: list):
    try: name = item[0]
    except: return None

    description = max(item, key=len)
    if ( "//" in description or "//" not in description and len(filter_text(description)) == 0 ): description = "-"

    website = next( (e.strip() for e in item if (isinstance(e, str) and e.startswith("http"))), None,)
    if website is None: return None

    return {"Name": name, "Description": description, "Website": website}


def get_advertiser_info_block( driver: webdriver.Chrome, index: int, number_of_elements: int ) -> BeautifulSoup:  # type: ignore
    
    xpath_head = "//*[@id='content']/div/div/div/div[5]/div[2]/div[2]/div[4]/div[1]/div"
    for xpath in get_xpath_for_each_element(xpath_head=xpath_head,
                                            start=index,
                                            number_of_elements=number_of_elements):

        try: parent_element = driver.find_element(By.XPATH, xpath)
        except: yield None

        element_xpath = find_company_name_element_xpath (parent_element=parent_element,
                                                         parent_element_xpath=xpath)

        if xpath is not None:
            try:
                element = driver.find_element(By.XPATH, element_xpath)
                yield hover_element(driver=driver, element=element, xpath=xpath)  # type: ignore
            except Exception: yield None

        yield None


############################################################################################################
########################################## Root scraping function ##########################################
############################################################################################################
def scrape_data(driver, index: int, number_of_elements: int):
    for info_block_text_list in get_advertiser_info_block(driver=driver, index=index, number_of_elements=number_of_elements):

        # Skip to the next iteration if info_block is None
        if info_block_text_list is None:
            print("WARNING: No information block found on hover.")
            continue
        
        # Extract company information from the info_block
        get_advertiser_text_list = get_advertiser_texts(info_block=info_block_text_list) # type: ignore
        company_information = extract_company_info(get_advertiser_text_list)

        # Skip to the next iteration if company_info is None
        if company_information is None:
            print("WARNING: No company data found.")
            continue

        print(f"Extracted data of company: {company_information['Name']} | Website link: {company_information['Website']}")
        yield company_information