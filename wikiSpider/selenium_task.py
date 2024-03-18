from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random

driver = webdriver.Chrome()
url_search = 'https://twitter.com/search?q=%23Selenium'
driver.get(url_search)

def title_source():
    #Get the page title:
    title = driver.title
    print('Title: ', title)
    
    #Get the page source:
    source = driver.page_source
    print('Page source', source)

title_source()

def hash_picker():
    #Waiting until twitter loads
    wait = WebDriverWait(driver, 10)
    wait.until(EC.title_contains("Twitter"))

    #finds the search bar and enters a '#'
    search_box = driver.find_element_by_xpath('//input[@data-testid="SearchBox_Search_Input"]')
    search_box.send_keys("#")

    #Wait for results to load
    search_box.send_keys(Keys.RETURN)
    driver.implicitly_wait(10)

    #Finding hashtags on the page
    hashtag_links = driver.find_elements_by_xpath('//a[@href][contains(@href, "hashtag")]')

    #Picking a random hashtag
    random_hashtag = random.choice(hashtag_links)

    #Clicking this hashtag
    random_hashtag.click()

for x in range(6):
    hash_picker()
    title_source()

#Closing webdriver
driver.quit()
