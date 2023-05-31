import sys
import logging
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils import check_if_more_data_available, get_total_results, initialize_chrome, scrape_data, write_list_of_dicts_to_csv

base_url = "https://www.facebook.com/ads/library/"
active_status = "active_status=all"
ad_type = "ad_type=all"
country = "country=IN"
query = "q=tech"
search_type = "search_type=keyword_unordered"
media_type = "media_type=all"

# driver
driver = initialize_chrome()

# get url
url = f"{base_url}?" + "&".join(
    [active_status, ad_type, country, query, search_type, media_type]
)
driver.get(url)

# wait for the elements to load
wait = WebDriverWait(driver, 15)
wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='content']/div/div/div/div[5]/div[2]/div[2]/div[4]/div[1]")))

# creating global variables
index, end = 1, get_total_results(driver=driver)
headers = ["name", "description", "website"]
data_list = []

# check if no data found
if end < index:
    print ("No data found with this query...")
    sys.exit()

while index < end:

    # scroll to the max height
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # scrape data
    for data in scrape_data(driver=driver, index=index, number_of_elements=30):
        data_list.append(data)
        index += 1

    # write scraped data into csv file and clear data list
    write_list_of_dicts_to_csv(headers=headers, data_list=data_list, filename="data/results.csv")
    data_list = []
    logging.info("saved data into csv file.")

    # check if more data available
    found = check_if_more_data_available(driver=driver, end=index)

    # loop to check if more data is available
    if not found:
        logging.info("checking if more data available!")
        while index < end:
            # Wait for 1 seconds and check again
            sleep(1)
            found = check_if_more_data_available(driver=driver, end=index)

            # break the loop if more data is available
            if found: break

driver.close()
sys.exit()


# requirements
# 1. company name
# 2. company description
# 3. advertising platforms
# 4. company website