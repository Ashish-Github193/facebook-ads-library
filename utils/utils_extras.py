import codecs
import csv

from scraper import platform_names_scraper

def get_headers_for_saving_data() -> list:

    # basic_information_scraper
    basic_information_scraper_headers = ["Name", "Type", "Description", "Website"]

    # platform_names_scraper
    platform_names_scraper_headers    = ["Facebook", "Instagram", "Audience Network", "Messenger", "Date"]

    return basic_information_scraper_headers + platform_names_scraper_headers


def write_list_of_dicts_to_csv(headers, data_list, filename):
    with codecs.open(filename, 'a', encoding='utf-8', errors='replace') as file:
        writer = csv.DictWriter(file, fieldnames=headers)

        # Check if the file is empty else write row
        if file.tell() == 0: writer.writeheader()
        writer.writerows(data_list)
    
    print(f'Data appended to {filename} successfully.')

def merge_dictionaries(dictionaries):
    merged_dict = {}
    for dictionary in dictionaries:
        merged_dict.update(dictionary) # type: ignore
    return merged_dict

def change_date_format(date):
    date = date.split('-')
    formatted_date = f"{date[1]}-{date[0]}"
    return formatted_date