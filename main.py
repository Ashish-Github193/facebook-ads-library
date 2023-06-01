# Modules
from time                            import sleep
from selenium.webdriver.common.by    import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support      import expected_conditions as EC

# Defined functions
from scraper.get_total_results       import get_total_found_results
from utils.utils_date_operations     import *
from utils.utils_initialise_function import *
from utils_scrape_data               import scrape_data
from utils.utils_frequent_function   import check_if_more_data_available
from utils.utils_extras              import get_headers_for_saving_data, write_list_of_dicts_to_csv


# initializing global variables
COUNTRY = "IN"
END_DATE = "2018-05-07"
MONTH_DIFFERENCE = 1
DATA_FOLDER_NAME = "data/"
MAX_ITERATION_PER_PAGE = 90

# Url keywords
base_url = "https://www.facebook.com/ads/library/"
active_status = "active_status=all"
ad_type = "ad_type=all"
country = f"country={COUNTRY}"
query = "q=tech"
search_type = "search_type=keyword_unordered"
media_type = "media_type=all"
start_date_min="start_date[min]="
start_date_max="start_date[max]="


start_date_max_itr = get_current_date()
start_date_min_itr = get_min_date(month_difference=1, max_date=start_date_max_itr)

while check_if_start_is_bigger(start_date=start_date_max_itr, end_date=END_DATE):

    # prepare date filter
    start_date = start_date_min + start_date_min_itr
    end_date   = start_date_max + start_date_max_itr

    # prepare url
    items_list = [active_status, ad_type, country, query, search_type, media_type, start_date, end_date]
    url = f"{base_url}?" + "&".join(items_list)

    # prepare driver
    driver = initialize_chrome()
    driver.get(url)

    # check if the main division found
    try:
        wait = WebDriverWait(driver, 15)
        wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[1]/div[1]/div/div/div/div[5]/div[2]/div[2]/div[4]/div[1]")))
    except Exception: continue

    # creating global variables
    advertiser_block_iteration_index     = 1
    advertiser_block_iteration_max_index = get_total_found_results (driver=driver)
    chunk_of_advertiser_data             = []

    # check if no companies found
    if advertiser_block_iteration_max_index < advertiser_block_iteration_index: continue

    print()
    print()
    print(f"URL: {url}")
    print(f"Scraping data from date: {start_date_min_itr} to date: {start_date_max_itr}", end="\n\n")

    # writing file name and looping the scraper
    filename = f"{COUNTRY}_{query}.csv"
    while advertiser_block_iteration_index < advertiser_block_iteration_max_index and advertiser_block_iteration_index < MAX_ITERATION_PER_PAGE:

        print()
        print(f"Iteration count: {advertiser_block_iteration_index}")

        # scrape data
        for advertiser_data in scrape_data(driver=driver,
                                           index=advertiser_block_iteration_index,
                                           number_of_elements=30):

            if advertiser_data is not None: chunk_of_advertiser_data.append(advertiser_data)
            advertiser_block_iteration_index += 1

        # write scraped data into csv file and clear data list
        write_list_of_dicts_to_csv(headers=get_headers_for_saving_data(),
                                   data_list=chunk_of_advertiser_data,
                                   filename=DATA_FOLDER_NAME+filename)
        chunk_of_advertiser_data = []

        # loop to check if more data is available
        while advertiser_block_iteration_index < advertiser_block_iteration_max_index and \
              advertiser_block_iteration_index < MAX_ITERATION_PER_PAGE and \
              not check_if_more_data_available(driver=driver, end=advertiser_block_iteration_index):

            sleep(1)

    # close the driver
    driver.close()

    # going back in time with month difference
    start_date_max_itr = start_date_min_itr
    start_date_min_itr = get_min_date(month_difference=1, max_date=start_date_max_itr)