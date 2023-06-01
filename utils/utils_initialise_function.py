from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def initialize_chrome() -> webdriver.Chrome:
    chrome_options = Options()
    chrome_options.add_argument('--incognito')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument('--blink-settings=imagesEnabled=false')
    return webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

