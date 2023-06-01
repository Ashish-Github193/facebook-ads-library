from contextlib                              import suppress
from selenium.webdriver.common.by            import By
from selenium.webdriver.remote.webelement    import WebElement

facebook_style         = "width: 12px; height: 12px; -webkit-mask-image: url('https://static.xx.fbcdn.net/rsrc.php/v3/yd/r/tuMP4thDyat.png'); -webkit-mask-size: 26px 716px; -webkit-mask-position: 0px -646px;"
instagram_style        = "width: 12px; height: 12px; -webkit-mask-image: url('https://static.xx.fbcdn.net/rsrc.php/v3/ym/r/wcAEKoUC9M5.png'); -webkit-mask-size: 30px 696px; -webkit-mask-position: -16px -58px;"
audience_network_style = "width: 12px; height: 12px; -webkit-mask-image: url('https://static.xx.fbcdn.net/rsrc.php/v3/ym/r/wcAEKoUC9M5.png'); -webkit-mask-size: 30px 696px; -webkit-mask-position: -16px -58px;"
messenger_style        = "width: 12px; height: 12px; -webkit-mask-image: url('https://static.xx.fbcdn.net/rsrc.php/v3/ym/r/wcAEKoUC9M5.png'); -webkit-mask-size: 30px 696px; -webkit-mask-position: -16px -58px;"

platforms = {
    "Facebook":         "false",
    "Instagram":        "false",
    "Audience Network": "false",
    "Messenger":        "false"
}

def get_advertising_platforms(parent_element: WebElement):
    
    with suppress(Exception):
        elements = parent_element.find_elements(By.TAG_NAME, "div")
        for element in elements:

            try: style = element.get_attribute("style")
            except: continue

            if   style == facebook_style:         platforms["Facebook"]         = "true"
            elif style == instagram_style:        platforms["Instagram"]        = "true"
            elif style == audience_network_style: platforms["Audience Network"] = "true"
            elif style == messenger_style:        platforms["Messenger"]        = "true"

        return platforms

    return None