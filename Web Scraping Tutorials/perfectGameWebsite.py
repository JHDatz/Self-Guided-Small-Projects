# Joe Datz
# 1/14/2020
# Big Problems
#
# This file is used as an explanation of how to web scrape highschool and college player
# information from the website perfectgame.org. We'll do this with the following steps:
#
#   1. Go to the main page of perfectgame and scrape every link that leads to an article.
#   2. Go to each article page, and scrape every link that leads to a player's profile page.
#   3. Go to each player's profile page to scrape various bits of information, and write this
#       back to a CSV file.
#
# The first thing we'll have to do is import the relevant tools. Here I have used:
#
# requests - to interact with perfectgame.org.
#
# bs4 - Shorthand for "BeautifulSoup, version 4.0," a library package for parsing the
#       HTML we'll get back from perfectgame.org.
#
# re  - Shorthand for "Regular Expressions," used to parse a python string for information
#       that we're looking for.

import requests
from bs4 import BeautifulSoup
import re

# This helper function will allow us to standardize the format of the profile links
# that we'll scrape. Specifically, it will pull out the 5 or 6 digit ID number
# out of a hyperlink that goes to a player's profile page.

def standardize_format(string): return re.search('[0-9]{5,6}$', string).group(0)

# Perfectgame is more hostile to web scrapers, so to make the program look more like a human
# we'll modify our headers. Headers are used as pieces of identifying information given to
# a web server to determine what kind of information should be sent back to the user making.
# Without modifying them, the 'User-Agent' stays as 'Python-requests' and looks much more like a bot.

headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.5',
           'Connection': 'keep-alive'}

response = requests.get('https://www.perfectgame.org/', headers=headers) # Get the HTML off of the page.

soup = BeautifulSoup(response.text, 'html.parser') # Use BeautifulSoup to parse the HTML on the page.

# There are a few things going on in this line of code:
#
#   1. The soup.find_all method is being used to parse through the page's HTML
#       and find all the hyperlinks with the phrase 'Articles' in them.
#   2. The articles['href'] is being used to parse remaining HTML and just be left with the hyperlink.
#   3. The articles are wrapped in a list comprehension to get all of these in one line of code.
#
# If you still feel confused about how this line works, google "python lambda expressions"
# or "python list comprehensions" and see if that helps.

links = [articles['href'] for articles in soup.find_all(lambda tag: 'href' in tag.attrs and 'Articles' in tag['href'])]

set_of_players = set() # This variable will be used to store all found players on each web page.

for articles in links:
    response = requests.get('https://www.perfectgame.org/' + articles, headers=headers) # Add the article hyperlink extensions.
    soupy = BeautifulSoup(response.text, 'html.parser') # Use BeautifulSoup to parse through the HTML.

    # In the same fashion as the Articles, lambda expressions, python comprehensions,
    # and BeautifulSoup are used together to filter down to just the player's
    # profile pages. The one addition is the use of our helper function
    # to keep a standard format.

    set_of_players = set_of_players.union({standardize_format(players['href']) for players in soupy.find_all(lambda tag: 'href' in tag.attrs and 'Playerprofile.aspx' in tag['href'])})

# info_locations is a list of HTML attributes that are the locations of content on a player's
# profile page that we'd like to scrape. Most are eponymous, but the more ambiguous are:
#
# 'ContentPlaceHolder1_lblPos' - Shorthand for position.
# 'ContentPlaceHolder1_hl4yearCommit' - The college a player has committed to.
# 'ContentPlaceHolder1_lblBestPGGrade' - A grade on a scale from 1 to 10.
# 'ContentPlaceHolder1_lblRankingNote' - Latest commentary given on a player's profile page.


info_locations = ['ContentPlaceHolder1_lblPlayerName', 'ContentPlaceHolder1_lblHSGrad', 'ContentPlaceHolder1_lblPos',
                  'ContentPlaceHolder1_lblRecentDraftedDate', 'ContentPlaceHolder1_hl4yearCommit',
                  'ContentPlaceHolder1_lblStateRank', 'ContentPlaceHolder1_lblStatePosRank',
                  'ContentPlaceHolder1_lblNationalRank', 'ContentPlaceHolder1_lblNationalPosRank',
                  'ContentPlaceHolder1_lblBestPGGrade',
                  'ContentPlaceHolder1_lblRankingNote']

file = open('pg_mentioned_players.csv', 'w') # Open the file we'll save our info to.
file.write('Name, Graduation, Position, Draft Date, College Commitment, State Rank, State Rank by Position,'
           'National Rank, National Rank by Position, PG Grade, Comments\n') # Write the column names as the first row.


for IDs in list(set_of_players):
    response = requests.get('https://www.perfectgame.org/Players/Playerprofile.aspx?ID=' + IDs, headers=headers) # Head to a player's profile page.

    soupish = BeautifulSoup(response.text, 'html.parser') # Use BeautifulSoup to parse the HTML in response.text.

    for locations in info_locations:

        # Use info_locations and soupish to parse through HTML for the information
        # that we'd like to collect.

        category = soupish.find_all(lambda tag: 'id' in tag.attrs and locations in tag['id'])

        # If soupish doesn't find the info, it's probably because this particular
        # player page doesn't have it. This if-else case here is used to write
        # NULLS so that the program doesn't crash otherwise.

        if len(category) != 0:
            category = category[0].text
        else:
            category = 'NULL'

        # Write the info to the CSV file. The if-else is used to determine
        # if we're writing to the first column or not.

        if locations == 'ContentPlaceHolder1_lblPlayerName':
            file.write(category.replace(',', ''))
        else:
            file.write(', ' + category.replace(',', ''))

    file.write('\n') # Begin the next row.

# We're done. Close the file.

file.close()


