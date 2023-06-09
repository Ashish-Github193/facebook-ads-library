import logging
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Importing utility functions and modules
from utils.utils_date_operations import *
from utils.utils_initialise_function import *
from utils.utils_user_handler import get_user_inputs
from utils_scrape_data import scrape_data
from utils.utils_frequent_function import check_if_more_data_available
from utils.utils_extras import (
    get_headers_for_saving_data,
    write_list_of_dicts_to_csv,
    change_date_format,
)
from scraper.get_total_results import total_advertisement_on_current_page

# Constants
END_DATE = "2020-05-07"
MONTH_DIFFERENCE = 1
DATA_FOLDER_NAME = "data/"
MAX_ITERATION_PER_PAGE = 150


# Function to prepare the URL by joining items in the items_list
def prepare_url(base_url, items_list):
    return f"{base_url}?" + "&".join(items_list)


# Function to scrape and write data to a CSV file
def scrape_and_write_data(
    driver,
    iteration_count,
    total_iterations_count,
    chunk_of_advertiser_data,
    date_started_in,
    filename,
):
    for advertiser_data in scrape_data(
        driver=driver, index=iteration_count, number_of_elements=30
    ):
        if advertiser_data is not None:
            advertiser_data["Date"] = change_date_format(date_started_in)
            chunk_of_advertiser_data.append(advertiser_data)
        iteration_count += 1

    write_list_of_dicts_to_csv(
        headers=get_headers_for_saving_data(),
        data_list=chunk_of_advertiser_data,
        filename=DATA_FOLDER_NAME + filename,
    )
    chunk_of_advertiser_data = []

    return iteration_count


# Function to check if more data is available on the page
def check_for_more_data(driver, total_iterations_count):
    check_itr = 0
    while (
        check_if_more_data_available(driver=driver, total=total_iterations_count)
        and check_itr != 10
    ):
        check_itr += 1
        sleep(1)


# Function to initialize the driver and load the URL
def initialize_driver(url):
    driver = initialize_chrome()
    driver.get(url)
    return driver


# Function to check if the main division is found on the page
def check_main_division(driver):
    try:
        wait = WebDriverWait(driver, 15)
        wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "/html/body/div[1]/div[1]/div[1]/div/div/div/div[5]/div[2]/div[2]/div[4]/div[1]",
                )
            )
        )
        return True
    except TimeoutError:
        # Handle timeout exception
        logging.error("Timeout exception occurred while waiting for the main division.")
        return False
    except Exception as e:
        # Handle other exceptions
        logging.error(f"An error occurred while checking the main division: {str(e)}")
        return False


# Function to scrape data based on the provided inputs
def scrape_data_with_inputs(country_code, ad_type, search_query):
    # URL keywords
    base_url = "https://www.facebook.com/ads/library/"
    active_status = "active_status=all"
    ad_type = f"ad_type={ad_type}"
    country = f"country={country_code}"
    query = f"q={search_query}"
    search_type = "search_type=keyword_unordered"
    media_type = "media_type=all"
    start_date_min = "start_date[min]="
    start_date_max = "start_date[max]="

    # Get the current date and the minimum date based on the month difference
    start_date_max_itr = get_current_date()
    start_date_min_itr = get_min_date(month_difference=1, max_date=start_date_max_itr)

    # Start scraping data until the start date is bigger than the end date
    while check_if_start_is_bigger(start_date=start_date_max_itr, end_date=END_DATE):
        # Prepare date filter
        start_date = start_date_min + start_date_min_itr
        end_date = start_date_max + start_date_max_itr

        # Prepare the URL
        items_list = [
            active_status,
            ad_type,
            country,
            query,
            search_type,
            media_type,
            start_date,
            end_date,
        ]
        url = prepare_url(base_url=base_url, items_list=items_list)

        # Initialize the driver and load the URL
        driver = initialize_driver(url)

        # Check if the main division is found on the page
        if not check_main_division(driver):
            driver.close()
            continue

        logging.info(f"URL: {url}")
        logging.info(
            f"Scraping data from date: {start_date_min_itr} to date: {start_date_max_itr}",
            end="\n\n",
        )

        # Set the filename and initialize variables
        filename = f"{country_code}_{search_query}.csv"
        chunk_of_advertiser_data = []
        iteration_count = 1
        total_iterations_count = MAX_ITERATION_PER_PAGE

        # Check if there are new data available on the page
        total_data_after_new_data_arrived = total_advertisement_on_current_page(
            driver=driver
        )
        if total_data_after_new_data_arrived - iteration_count < 29:
            total_iterations_count = total_data_after_new_data_arrived

        # Start iterating over the data on the page
        while iteration_count < total_iterations_count:
            logging.info(
                f"\nIteration start; total_data: {total_iterations_count}; iteration count: {iteration_count};"
            )

            # Scrape and write data to CSV
            iteration_count = scrape_and_write_data(
                driver,
                iteration_count,
                total_iterations_count,
                chunk_of_advertiser_data,
                start_date_min_itr,
                filename,
            )

            # Check for more data
            check_for_more_data(driver, total_iterations_count)

            # Check if there are new data available on the page
            total_data_after_new_data_arrived = total_advertisement_on_current_page(
                driver=driver
            )
            if total_data_after_new_data_arrived - iteration_count < 29:
                total_iterations_count = total_data_after_new_data_arrived

        driver.close()

        # Update the start and end dates for the next iteration
        start_date_max_itr = start_date_min_itr
        start_date_min_itr = get_min_date(
            month_difference=1, max_date=start_date_max_itr
        )


# Entry point of the script
if __name__ == "__main__":
    # Get user inputs
    country_code, ad_type, search_query = get_user_inputs().split("-")
    # Call the scrape_data_with_inputs function
    scrape_data_with_inputs(
        country_code=country_code, ad_type=ad_type, search_query=search_query
    )
