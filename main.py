import logging
from time import sleep
from math import inf
from random import randint
from pytz import country_names
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.utils_date_operations import *
from utils.utils_initialise_function import *
from utils.utils_user_handler import get_user_inputs
from utils_scrape_data import scrape_data
from utils.utils_frequent_function import check_if_more_data_available
from utils.utils_extras import get_headers_for_saving_data, write_list_of_dicts_to_csv
from scraper.get_total_results import total_advertisement_on_current_page

END_DATE = "2018-05-07"
MONTH_DIFFERENCE = 1
DATA_FOLDER_NAME = "data/"
MAX_ITERATION_PER_PAGE = 150

def prepare_url(base_url, items_list):
    return f"{base_url}?" + "&".join(items_list)

def scrape_and_write_data(driver, iteration_count, total_iterations_count, chunk_of_advertiser_data, filename):
    for advertiser_data in scrape_data(driver=driver, index=iteration_count, number_of_elements=30):
        if advertiser_data is not None:
            chunk_of_advertiser_data.append(advertiser_data)
        iteration_count += 1

    write_list_of_dicts_to_csv(headers=get_headers_for_saving_data(),
                               data_list=chunk_of_advertiser_data,
                               filename=DATA_FOLDER_NAME + filename)
    chunk_of_advertiser_data = []

    return iteration_count

def check_for_more_data(driver, total_iterations_count):
    check_itr = 0
    while check_if_more_data_available(driver=driver, total=total_iterations_count) and check_itr != 10:
        check_itr += 1
        sleep(1)

def main(country_code, ad_type, search_query):

    # Url keywords
    base_url         =  "https://www.facebook.com/ads/library/"
    active_status    =  "active_status=all"
    ad_type          = f"ad_type={ad_type}"
    country          = f"country={country_code}"
    query            = f"q={search_query}"
    search_type      =  "search_type=keyword_unordered"
    media_type       =  "media_type=all"
    start_date_min   =  "start_date[min]="
    start_date_max   =  "start_date[max]="

    start_date_max_itr = get_current_date()
    start_date_min_itr = get_min_date(month_difference=1, max_date=start_date_max_itr)

    while check_if_start_is_bigger(start_date=start_date_max_itr, end_date=END_DATE):

        # prepare date filter
        start_date = start_date_min + start_date_min_itr
        end_date   = start_date_max + start_date_max_itr

        # prepare url
        items_list = [active_status, ad_type, country, query, search_type, media_type, start_date, end_date]
        url        = prepare_url(base_url=base_url, items_list=items_list)

        # prepare driver
        driver = initialize_chrome()
        driver.get(url)

        # check if the main division found
        try:
            wait = WebDriverWait(driver, 15)
            wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[1]/div[1]/div/div/div/div[5]/div[2]/div[2]/div[4]/div[1]")))
        except Exception: continue

        print()
        print()
        print(f"URL: {url}")
        print(f"Scraping data from date: {start_date_min_itr} to date: {start_date_max_itr}", end="\n\n")

        filename = f"{country_code}_{search_query}.csv"
        chunk_of_advertiser_data = []
        iteration_count = 1
        total_iterations_count = MAX_ITERATION_PER_PAGE

        total_data_after_new_data_arrived = total_advertisement_on_current_page(driver=driver)
        if total_data_after_new_data_arrived - iteration_count < 29:
            total_iterations_count = total_data_after_new_data_arrived

        while iteration_count < total_iterations_count:
            logging.info(f"\nIteration start; total_data: {total_iterations_count}; iteration count: {iteration_count};")

            iteration_count = scrape_and_write_data(driver, iteration_count, total_iterations_count,
                                                    chunk_of_advertiser_data, filename)

            check_for_more_data(driver, total_iterations_count)

            total_data_after_new_data_arrived = total_advertisement_on_current_page(driver=driver)
            if total_data_after_new_data_arrived - iteration_count < 29:
                total_iterations_count = total_data_after_new_data_arrived

        driver.close()

        start_date_max_itr = start_date_min_itr
        start_date_min_itr = get_min_date(month_difference=1, max_date=start_date_max_itr)

if __name__ == "__main__":
    country_code, ad_type, search_query = get_user_inputs().split('-')
    main(country_code=country_code, ad_type=ad_type, search_query=search_query)
