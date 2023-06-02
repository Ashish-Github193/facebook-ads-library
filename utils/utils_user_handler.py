import csv
import re
import pandas as pd

def show_country_codes():
    country_codes = pd.read_csv("data/all_country_codes.csv")
    print(country_codes.to_markdown())


def get_country_code():
    # Input country code
    country_code = input('\nPlease input the country code: ')

    with open('data/all_country_codes.csv', 'r') as file:
        csv_reader = csv.DictReader(file)
        valid_country_codes = [row['alpha-2'] for row in csv_reader]

    while country_code not in valid_country_codes:
        print(f"Invalid country code: '{country_code}'")
        country_code = input('\nPlease input the country code \'again\': ')

    return country_code


def get_ad_type():
    # Input ad type
    ad_type = input("""\nThere are two types of ads:
                        1. All ads
                        2. Political ads
                        
                       Please type '1' to select 'All ads' and '2' for 'Politics' related ads: """)

    while not re.match(r'^[1-2]$', ad_type):
        print("Invalid ad type. Please select '1' or '2'.")
        ad_type = input("\nPlease type '1' for 'All ads' or '2' for 'Politics' related ads: ")

    ad_type = 'all' if ad_type == '1' else 'political_and_issue_ads'

    return ad_type

def get_query():
    # Input query
    query = input('\nEnter any search query to search ads by keyword or advertiser: ')
    while not re.match(r'^[a-zA-Z0-9\s]+$', query):
        print("Invalid query. Only alphanumeric characters and spaces are allowed.")
        query = input("\nEnter a valid search query: ")
    
    return query

def get_user_inputs():
    # Write instructions
    instructions = '''Welcome to the Selenium-Facebook-ads-library-scraper!

    In this tool, you can explore and select any country from a comprehensive list using
    their respective alpha-2 country codes. The alpha-2 codes are two-letter codes that represent
    each country, making it easy to identify and locate a specific nation.

    The list of countries that Facebook Ads Library supports will be shown below.
    Once you've identified the alpha-2 country code for your desired country, select it by clicking
    or tapping on it. This selection will trigger the retrieval of detailed information about
    the country you chose.'''
    print(instructions)

    # Show all country data
    ask_to_show_country_codes = input("\nType 'y' to see country codes and 'z' to cancel: ")
    if bool(re.search(r'[a-y]', ask_to_show_country_codes, re.IGNORECASE)):
        show_country_codes()

    country_code = get_country_code()
    ad_type      = get_ad_type()
    query        = get_query()

    return f"{country_code}-{ad_type}-{query}"