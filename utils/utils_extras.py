import codecs, csv, os


def get_headers_for_saving_data() -> list:
    # basic_information_scraper
    basic_information_scraper_headers = ["Name", "Type", "Description", "Website"]

    # platform_names_scraper
    platform_names_scraper_headers = [
        "Facebook",
        "Instagram",
        "Audience Network",
        "Messenger",
        "Date",
    ]

    return basic_information_scraper_headers + platform_names_scraper_headers

def delete_all_file_from_data_dir (directory):
    files = os.listdir(directory)

    # Iterate through each file in the directory
    for file in files:
        file_path = os.path.join(directory, file)
        
        # Check if the current file is the file you want to keep
        if file != 'all_country_codes.csv':
            os.remove(file_path)
            print(f"Deleted existing file: {file_path}",)
        else:
            print(f"Kept file: {file_path}", end='\n\n')


def write_list_of_dicts_to_csv(headers, data_list, filename):
    with codecs.open(filename, "a", encoding="utf-8", errors="replace") as file:
        writer = csv.DictWriter(file, fieldnames=headers)

        # Check if the file is empty else write row
        if file.tell() == 0:
            writer.writeheader()
        writer.writerows(data_list)

    print(f"Data saved successfully in {filename}")


def merge_dictionaries(dictionaries):
    merged_dict = {}
    for dictionary in dictionaries:
        merged_dict |= dictionary
    return merged_dict


def change_date_format(date):
    date = date.split("-")
    return f"{date[1]}-{date[0]}"

def show_ip_block_message():
    return '''Error while checking the main division.

It has come to our attention that your current activity on Facebook is proceeding
at an accelerated rate. As a result, your IP address has been blocked by Facebook
due to the excessive number of page requests made within a very short period. Please note
that this block is temporary in nature, which means that your IP will remain restricted
for a duration ranging from 8 to 24 hours.

To confirm the status of your IP address, we recommend running the scraper tool again on the
following day. If, despite the passage of time, you still encounter the same issue and find that
your IP address remains blocked, please get in touch with developer team.'''