import sys, getopt
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# Write the scrawled data in file
def writeFileTxt(fileName, content):
    with open(fileName, 'a', encoding="utf-8") as f1:
        f1.write(content + os.linesep)

# Read the list of search keys from file
def readData(fileName):
    f = open(fileName, 'r', encoding='cp949')
    lines = f.readlines()
    data = [line.rstrip() for line in lines if line.rstrip() != '']
    return data

# Initialize the chromedriver
def initDriver():
    CHROMEDRIVER_PATH = './chromedriver.exe'
    WINDOW_SIZE = "1900,2500"
    chrome_options = Options()
    chrome_options.binary_location = "C:/Program Files (x86)/Google/Chrome Beta/Application/chrome.exe"
    #chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('disable-infobars')
    chrome_options.add_argument('--disable-gpu') if os.name == 'nt' else None  # Windows workaround
    chrome_options.add_argument("--verbose")
    chrome_options.add_argument("--no-default-browser-check")
    chrome_options.add_argument("--ignore-ssl-errors")
    chrome_options.add_argument("--allow-running-insecure-content")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--disable-feature=IsolateOrigins,site-per-process")
    chrome_options.add_argument("--no-first-run")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-translate")
    chrome_options.add_argument("--ignore-certificate-error-spki-list")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--disable-blink-features=AutomationControllered")
    chrome_options.add_experimental_option('useAutomationExtension', False)
    prefs = {"profile.default_content_setting_values.notifications": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument("--start-maximized")  # open Browser in maximized mode
    chrome_options.add_argument("--disable-dev-shm-usage")  # overcome limited resource problems
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
    chrome_options.add_argument('disable-infobars')

    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH,
                              options=chrome_options
                              )
    return driver

# Collect all the data from naver.com
def getInformation(driver, search_key, number_of_pages = 2):
    try:
        main_page = "https://search.naver.com/search.naver?where=view&sm=tab_jum&query=" + search_key;
        driver.get(main_page)
        link_list = driver.find_elements_by_xpath('//a[contains(@class, "api_txt_lines total_tit")]')
        links = [link.get_attribute('href') for link in link_list]
        count = 1
        for link in links:
            driver.get(link)
            # Switch to frame to collect the data of a frame
            driver.switch_to.frame("mainFrame")
            content_list = driver.find_elements_by_xpath('//span[contains(@class, "se-fs- se-ff-")]')
    
            contents = [content.text.strip() for content in content_list if content.text.strip() != '']

            fileName = "dataset/" + search_key + "-" + str(count) + ".txt"
            
            writeFileTxt(fileName,"\n".join(contents))
            if (count == number_of_pages): 
                break
            count += 1
    except Exception as err:
        print("Error getting food information: ", err)

# Check whether the driver is launched well
def checkLive(driver):
    try:
        driver.get("https://www.naver.com/")
        sleep(2)
        elementLive = driver.find_elements_by_xpath('//a[contains(@href, "https://mail.naver.com/")]')
        if (len(elementLive) > 0):
            print("Live")
            return True

        return True
    except:
        print("Check Live Fail")

def main(argv):
    pageName = ''
    totalPost = 0

    # Initialize the chrome driver
    driver = initDriver()

    # Check the browser initialization
    isLive = checkLive(driver)

    if (not isLive):
        return

    try:
        opts, args = getopt.getopt(argv,"hf:s:n:",["fName", "skey=", "npage="])
    except getopt.GetoptError:
        print('python index.py -f <data file> -s <search key> -n <number of pages>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('python index.py -f <data file> -s <search key> -n <number of pages>')
            sys.exit()
        elif opt == '-f':
            fileName = arg
            list_search_keys = readData(fileName)
            for search_key in list_search_keys:
                print("Search key: ", search_key)
                getInformation(driver, search_key, 2)
                
            sys.exit()
        elif opt in ("-s", "--skey"):
            search_key = arg
        elif opt in ("-n", "--npage"):
            number_pages = int(arg)

    print("Search key: ", search_key)

    if (isLive):
        getInformation(driver, search_key, number_pages)


if __name__ == "__main__":
   main(sys.argv[1:])