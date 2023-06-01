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


def get_advertising_platforms(parent_element: WebElement):
    facebook_style = "width: 12px; height: 12px; -webkit-mask-image: url('https://static.xx.fbcdn.net/rsrc.php/v3/yd/r/tuMP4thDyat.png'); -webkit-mask-size: 26px 716px; -webkit-mask-position: 0px -646px;"
    instagram_style = "width: 12px; height: 12px; -webkit-mask-image: url('https://static.xx.fbcdn.net/rsrc.php/v3/ym/r/wcAEKoUC9M5.png'); -webkit-mask-size: 30px 696px; -webkit-mask-position: -16px -58px;"
    audience_network_style = "width: 12px; height: 12px; -webkit-mask-image: url('https://static.xx.fbcdn.net/rsrc.php/v3/ym/r/wcAEKoUC9M5.png'); -webkit-mask-size: 30px 696px; -webkit-mask-position: -16px -58px;"
    messenger_style = "width: 12px; height: 12px; -webkit-mask-image: url('https://static.xx.fbcdn.net/rsrc.php/v3/ym/r/wcAEKoUC9M5.png'); -webkit-mask-size: 30px 696px; -webkit-mask-position: -16px -58px;"

    platforms = {
        "Facebook": "false",
        "Instagram": "false",
        "Audience Network": "false",
        "Messenger": "false"
    }

    try:
        elements = parent_element.find_elements(By.TAG_NAME, "div")
    except Exception as e:
        print(e)
        return None

    for element in elements:
    
        try: style = element.get_attribute("style")
        except: continue

        if   style == facebook_style:         platforms["Facebook"]         = "true"
        elif style == instagram_style:        platforms["Instagram"]        = "true"
        elif style == audience_network_style: platforms["Audience Network"] = "true"
        elif style == messenger_style:        platforms["Messenger"]        = "true"

    return platforms


def get_advertiser_texts(info_block: BeautifulSoup):
    elements = info_block.find_all(text=True)
    return [e.get_text() for e in elements]


def extract_advertiser_info(item: list):
    try: name = item[0]
    except: return None

    description = max(item, key=len)
    if ( "//" in description or "//" not in description and len(filter_text(description)) == 0 ): description = "-"

    website = next( (e.strip() for e in item if (isinstance(e, str) and e.startswith("http"))), None,)
    if website is None: return None

    return {"Name": name, "Description": description, "Website": website}


def get_advertiser_information ( driver: webdriver.Chrome, index: int, number_of_elements: int ) -> BeautifulSoup:  # type: ignore
    
    xpath_head = "//*[@id='content']/div/div/div/div[5]/div[2]/div[2]/div[4]/div[1]/div"
    for advertisement_block_xpath in get_xpath_for_each_element(xpath_head=xpath_head,
                                                                start=index,
                                                                number_of_elements=number_of_elements):

        try: parent_element = driver.find_element(By.XPATH, advertisement_block_xpath)
        except: yield None, None

        advertiser_information_raw = get_advertiser_information_with_information_block (driver=driver,
                                                                                        parent_element=parent_element,
                                                                                        advertisement_block_xpath=advertisement_block_xpath)
        advertising_platforms      = None

        # if advertiser information found then get advertising platforms 
        if advertiser_information_raw is not None:
            advertising_platforms = get_advertising_platforms(parent_element=parent_element)

        yield advertiser_information_raw, advertising_platforms

############################################################################################################
########################################## Root scraping function ##########################################
############################################################################################################
def scrape_data(driver, index: int, number_of_elements: int):
    for advertiser_information_raw, advertising_platforms in get_advertiser_information (driver=driver,
                                                                                               index=index,
                                                                                               number_of_elements=number_of_elements):

        # Skip to the next iteration if info_block is None
        if advertiser_information_raw is None: continue
        
        # Extract advertiser information from the info_block
        info_block=advertiser_information_raw
        get_advertiser_text_list = get_advertiser_texts(info_block=info_block)
        advertiser_information = extract_advertiser_info(get_advertiser_text_list)

        # Skip to the next iteration if advertiser_info is None
        if advertiser_information is None: continue
        
        if advertising_platforms is not None:
            advertiser_information.update(advertising_platforms)
        # print(f"Extracted data of advertiser: {advertiser_information['Name']} | Website link: {advertiser_information['Website']}")
        yield advertiser_information