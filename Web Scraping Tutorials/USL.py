import time
from selenium import webdriver
from bs4 import BeautifulSoup
import csv

# Use geckodriver to create a web browser controlled by python. Go to page
# and wait a few seconds for Javascript to load on page.

driver = webdriver.Firefox(executable_path="/home/joseph/Desktop/pycharm/geckodriver")
driver.get("https://www.uslchampionship.com/northcarolinafc-loudoununitedfc-1036999")
time.sleep(4)

# Locate the in-game commentary with a CSS selector and convert to HTML.
# Hand this over to a BeautifulSoup object for HTML parsing.

relevant_html = driver.find_element_by_css_selector('ul.Opta-Striped').get_attribute("innerHTML")
soup = BeautifulSoup(relevant_html, 'html.parser')

# Filter out junk to get a timestamp column and a comments column. Use the
# zip() function to convert to a 2D List.

timestamps = [tags.getText().strip() for tags in soup.find_all('span', {'class': "Opta-Time"})]
comments = [tags.getText().strip() for tags in soup.find_all('span', {'class': 'Opta-comment'})]
wrapped = zip(timestamps, comments)

# Write to a CSV file.

with open('USLOutput.csv', 'w+') as f:
    writer = csv.writer(f)
    writer.writerow(['timestamp', 'comment'])
    writer.writerows(list(wrapped))