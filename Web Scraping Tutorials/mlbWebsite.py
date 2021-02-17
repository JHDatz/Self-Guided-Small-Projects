# Joe Datz
# 1/13/2020
# Big Problems
#
# This file is an explanation of the methodology used to web-scrape MLB.com of the information on its
# advertised minor league players.
#
# In a nutshell, we'll take the following steps to make it happen:
#
#   1. Go the MLB.com page for a list of best Minor League players.
#   2. Scrape an ID# for each player off each player.
#   3. Use this ID# to access a hidden webpage that contains all the information we were looking for.
#   4. Write this information onto a CSV file.
#
# The "hidden webpage" is an address to a JSON file. This file
# was found using the "developer tools" that are available on any browser
# and going to the "network" tab. The network tab shows the hidden interactions
# between a webserver and your computer, some of which include the information
# that we're after.
#
# The first thing we must do is import the relevant tools. Here I have used:
#
# selenium - General purpose web-scraping. The webpage for the minor league players loads
# dynamically like facebook; i.e not all information is available upon immediately loading
# of the page, and requires some button-pressing and scrolling. Selenium is good for
# handling this type of problem.
#
# selenium is not technically needed for this page over requests/urllib, but is done this
# way for demo purposes.
#
# time - to slow down accessing the webpages. If the webpage is not fully loaded, python will
# miss out on the information that is not rendered on the webpage.
#
# json - for reading JSON files into a nice format.
#
# urllib - to receive JSON files from MLB.com.
#
# re - regular expressions, to parse through information on the received files that I'd like.
#
# bs4 - Shorthand for "BeautifulSoup, version 4.0," a library package for parsing HTML.

from bs4 import BeautifulSoup
import time
import json
from urllib.request import urlopen
import re
from selenium import webdriver

# This creates a python-controlled version of Firefox.

driver = webdriver.Firefox()

# Open a file that we're going to write the data to.
#
# I've chosen to write a CSV file because the rules to creating one are simple:
#   1. Each column creates a comma in a spreadsheet.
#   2. Each '\n' character creates a new row in a spreadsheet.
#
# Microsoft Excel immediately recognizes this file type and will open it
# up like a regular excel spreadsheet.

file = open('mlb_top_prospects.csv', 'w')

# mlb_interwebz is a list of website extensions on MLB.com. For example:
#
# http://m.mlb.com/prospects/2019/?list=prospects, for top 100 minor league players.
# http://m.mlb.com/prospects/2019/?list=int, for top international players.
#
# This list is made so that a for-loop can be used over different webpages.

mlb_interwebz = ['prospects', 'int', 'ari', 'atl', 'bal', 'bos', 'chc', 'cws', 'cin', 'cle',
                    'col', 'det', 'hou', 'kc', 'ana', 'la', 'mia', 'mil', 'min', 'nym', 'nyy', 'oak',
                    'phi', 'pit', 'sd', 'sf', 'sea', 'stl', 'tb', 'tex', 'tor', 'was', 'rhp', 'lhp',
                    'c', '1b', '2b', '3b', 'ss', 'of']

# Write the first row of the CSV file as the definitions of each column.
# The definitions are as follows:
#
# year - the year that the player made a top 100 / top 30 / etc list.
#
# MLBAMID - a hidden ID# on MLB.com that identifies each player.
#
# Firstname - a player's first name.
#
# Lastname - a player's last name.
#
# ETA - A prediction of when MLB believes this player will transition from
# a minor league player to a major league player.
#
# isPitcher - designating whether or not this player is a pitcher. Players that are
# pitchers are being graded differently than a non-pitcher.
#
# Skill 1 Grade, Skill 2 Grade etc. - Baseball players are graded on a 20-80 scale
# for a particular ability that they have. This scale is quasi-normally distributed,
# with "50" as the mean with a standard deviation of 10. Since this demonstration is for web scraping,
# we won't go into much further detail with this.
#
# I've left these as "Skill 1" or "Skill 2" so that the pitchers and non-pitchers can
# use the same column.
#
# Overall - A 20-80 overall grade of a player's skills.
#
# Commentary - Whatever notes have been written about a player.

file.write('Year, MLBAMID, Firstname, Lastname, ETA, isPitcher, Skill 1 Grade, Skill 2 Grade, Skill 3 Grade, \
           Skill 4 Grade, Skill 5 Grade, Overall, Commentary\n')

# The for-loop for year is made to access different top 100 / 30 / etc
# from different years of baseball.

for year in ['2015', '2016', '2017', '2018', '2019']:

    for site_address in mlb_interwebz:
        driver.get('http://m.mlb.com/prospects/' + year + '/?list=' + site_address) # access the webpage in Selenium.
        time.sleep(3) # Wait 3 seconds for the web page to load.

        # There are two steps to this next line of code:
        #   1. driver.page_source is used to take all the information on the page as HTML.
        #   2. A BeautifulSoup object is created to parse the HTML in driver.page_source for the information we'd like.

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # There are a few steps to this line of code:
        #
        #   1. The soup.find_all method is used with a lambda expression to filter out
        #   pieces of HTML we don't want. We only want the ID#s of each player in this
        #   step, so all other information is irrelevant.
        #
        #   2. The soup.find_all method still gives the ID#s in the form of a python
        #   dictionary of HTML code, so the statement player_info['data-player-id']
        #   eliminates this to leave us with the 6-digit ID#s only.
        #
        #   3. This is wrapped in a set comprehension so that we can get all ID#'s
        #   in one line of python code.
        #
        #   A "set" instead of a "list" comprehension is used here because the MLB page
        #   gives two copies of an ID# for some reason. Using a "set" gets rid of the
        #   duplicate.
        #
        # If you are still not comfortable that you've understood what this piece of code is doing,
        # google "python list comprehension" and "lambda expression" to see if this helps you.

        playerid = {player_info['data-player-id'] for player_info in soup.find_all(lambda tag: 'data-player-id' in tag.attrs)}

        # We now have all the player ID#s. To get the data, we'll need to access another webpage
        # That is hidden in the background of MLB.com:
        #
        # http://m.mlb.com/gen/players/prospects/2019/677551.json
        #
        # The "677551" is the player's hidden ID# that we got a set of in the last line
        # of code. We will use the the IDs in a for-loop to grab data we'd like off of these JSON webpages.

        for ids in playerid:

            # Request the JSON file from the webpage. urlopen is used instead of requests.get here because
            # requests.get does not handle non-HTML information well.
            #
            # Technically Selenium's "driver" object can be used here as well, but I've stuck
            # to the json library because it is more convenient for parsing data.

            response = urlopen('http://m.mlb.com/gen/players/prospects/' + year + '/' + ids + '.json').read().decode('utf-8')

            player_info = json.loads(response) # Use the json package to handle JSON files.

            # Typically, the json package returns JSON files as a python dictionary.
            # These next few lines are to parse out the firstname, lastname, etc from
            # the file.

            player_firstname = player_info['prospect_player']['player_first_name']
            player_lastname = player_info['prospect_player']['player_last_name']
            player_mlbam_id = player_info['prospect_player']['player_id']
            player_eta = player_info['prospect_player']['eta']

            # BeautifulSoup is used to get the player's notes because there is some lingering HTML
            # I'd like to get rid of.

            soupy = BeautifulSoup(player_info['prospect_player']['content']['default'], 'html.parser')
            player_commentary = soupy.get_text().replace('\n', ' ')

            player_commentary = player_commentary.replace('\n', '')

            # Write the year, MLBAMID, firstname, lastname, and ETA to the CSV file.

            file.write(year + ', ' + str(player_mlbam_id) + ', ' + player_firstname + ', ' + player_lastname + ', '
                       + str(player_eta) + ', ')

            # This if-else and for-loop combination does the following:
            #   1. Check to see if a player is a pitcher or not using the JSON file. Write
            #       '1' for a pitcher and '0' otherwise.
            #
            #   2. Use the re package to parse out the 20-80 grades from the player_commentary variable.
            #       These are then used to fill out the Skill grade columns. Overall is intentionally
            #       kept as the last column.

            if player_info['prospect_player']['positions'] not in ['LHP', 'RHP']:
                file.write('0, ')
                for categories in ['Hit', 'Power', 'Run', 'Arm', 'Field', 'Overall']:
                    player_category = re.search(categories + ': [0-9]{2}', player_commentary)
                    if player_category is not None:
                        player_category = player_category.group(0).split(' ')[1]
                    else:
                        player_category = 'NULL'
                    file.write(player_category + ', ')
            else:
                file.write('1, ')
                for categories in ['Fastball', 'Curveball', 'Slider', 'Changeup', 'Control', 'Overall']:
                    player_category = re.search(categories + ': [0-9]{2}', player_commentary)
                    if player_category is not None:
                        player_category = player_category.group(0).split(' ')[1]
                    else:
                        player_category = 'NULL'
                    file.write(player_category + ', ')

            # Finish by writing the player_commentary as the last column, and use the '\n' to initiate a new row
            # for a new player.

            file.write(player_commentary.replace(',', '').replace('WATCH', '').replace('  ', ' ') + '\n')

# We're done. Close the file.

file.close()

# Exit out of Firefox.

driver.quit()
