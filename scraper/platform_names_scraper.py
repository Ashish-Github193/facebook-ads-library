from typing                                  import Dict, Optional
from contextlib                              import suppress
from selenium.webdriver.common.by            import By
from selenium.webdriver.remote.webelement    import WebElement

def find_platform_count(parent_element: WebElement) -> int:
    with suppress(Exception):
        sibling = parent_element.find_element(By.XPATH, "//span[text()='Platforms']/following-sibling::*")
        platform_count = len(sibling.find_elements(By.XPATH, "./*"))
        return platform_count

    return 0

def update_platforms_count(platforms: Dict[str, str], platform_count: int) -> Dict[str, str]:
    keys = list(platforms.keys())
    for platform in keys[:platform_count]: platforms[platform] = 'true'
    return platforms

def get_advertising_platforms(parent_element: WebElement) -> Optional[Dict[str, str]]:

    platform_count = find_platform_count(parent_element)
    if platform_count == 0: return None

    platforms = {
        "Facebook":         "false",
        "Instagram":        "false",
        "Audience Network": "false",
        "Messenger":        "false"
    }

    return update_platforms_count(platforms, platform_count)