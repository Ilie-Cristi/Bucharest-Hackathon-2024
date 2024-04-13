from selenium import webdriver


def getSS(url):
    driver = webdriver.Chrome()
    driver.get(url)
    driver.maximize_window()
    screenshot_base64 = driver.get_screenshot_as_base64()
    driver.quit()

    return screenshot_base64
