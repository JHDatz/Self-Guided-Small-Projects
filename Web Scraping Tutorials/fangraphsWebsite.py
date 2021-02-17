# Joe Datz
# 1/13/2020
# Big Problems
#
# This file is an explanation of the methodology used to webscrape fangraphs.com of the information on
# advertised minor league players.
#
# Fangraphs actively wants its readers to download and analyze it's information, so we'll
# do the following straightforward steps:
#
#   1. Open up a webpage with Selenium.
#   2. Use Selenium to press the "Download" button on the webpage for a CSV file.
#
# Admittedly this is a little trivial and doesn't need to done by a computer program. This is purely
# for demo purposes.
#
# CSV files are a common enough and useful file format that Microsoft Excel
# will recognize this and open this as any other spreadsheet.

# The first thing we must do is import the relevant tools. Here I have used:
#
# selenium - General purpose web-scraping. The webpage for Fangraph's top players loads
# dynamically like facebook; i.e not all information is available upon immediately loading
# of the page, and requires some button-pressing and scrolling. Selenium is good for
# handling this type of problem.
#
# time - to slow down accessing the webpages. If the webpage is not fully loaded, python will
# miss out on the information that is not rendered on the webpage.

import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

# On Firefox, pressing the 'download' button creates a prompt that
# makes sure you definitely want to download this thing. This code
# prevents that popup so that the web scraper can keep going.

firefoxProfile = FirefoxProfile()
firefoxProfile.set_preference("browser.download.folderList",1)
firefoxProfile.set_preference("browser.download.manager.showWhenStarting",False)
firefoxProfile.set_preference("browser.helperApps.neverAsk.saveToDisk","text/csv, application/csv")

# This creates a python-controlled version of Firefox.
# The profile is added so that it becomes part of the "driver" object,
# preventing the download prompt.

driver = webdriver.Firefox(firefox_profile=firefoxProfile)

# A list of webpages that we'd like to download files from.
#
# Luckily, the "download" button is at the same location of each page.
# This means we don't have to store 6 different addresses for where
# the "download" button is located on the page.

the_interwebz = ['https://www.fangraphs.com/prospects/the-board/2020-mlb-draft/summary?sort=-1,1&type=0',
            'https://www.fangraphs.com/prospects/the-board/2021-mlb-draft/summary?sort=-1,1&type=0',
            'https://www.fangraphs.com/prospects/the-board/2022-mlb-draft/summary?sort=-1,1&type=0',
            'https://www.fangraphs.com/prospects/the-board/2019-international/summary?sort=-1,1&type=0',
            'https://www.fangraphs.com/prospects/the-board/2019-premier12/summary?sort=-1,1&type=0',
            'https://www.fangraphs.com/prospects/the-board/2020-prospect-list/summary?sort=-1,1&type=0']

for pages in the_interwebz:
    driver.get(pages) # get to the webpage.
    time.sleep(5) # take 5 seconds to let the webpage load.

    # The next few lines of code depend on the XML markup language.
    # XML is similar to HTML in the sense that it functions as a way
    # to order information on a webpage. The elongated strings of XML
    # in the driver.find_element_by_xpath were found using the "developer
    # tools" that can be used on any browser. To get an XML address,
    # right click on the HTML in "developer tools" that corresponds
    # to the information on the page that you'd like, go down to
    # the "copy" option, and select the "XPath" option.

    try:
        driver.find_element_by_xpath('/html/body/div[4]/div[1]/div[3]/a[2]') # Say 'no thanks' to a pop-up ad.
        driver.execute_script("window.scrollTo(0, 500)") # Scroll down the page a bit so that the "download" button is in view.
        driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div[3]/a').click() # Press the "download" button.
    except NoSuchElementException: # This case added in case the pop-up ad does not exist.
        driver.execute_script("window.scrollTo(0, 500)") # Scroll down the page a bit so that the "download" button is in view.
        driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div/div[3]/a').click() # Press the "download" button.

# We're done. Exit out of Firefox.

driver.quit()
