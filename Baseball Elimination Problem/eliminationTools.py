import datetime
import pandas as pd
from pybaseball import schedule_and_record, standings

shorthands = {'Toronto Blue Jays': 'TOR', 'Milwaukee Brewers': 'MIL', 'Baltimore Orioles': 'BAL', 'Cleveland Indians': 'CLE', 'New York Yankees': 'NYY',
              'Detroit Tigers': 'DET', 'Boston Red Sox': 'BOS', 'Oakland Athletics': 'OAK', 'Minnesota Twins': 'MIN', 'Chicago White Sox': 'CHW',
              'Texas Rangers': 'TEX', 'California Angels': 'CAL', 'Kansas City Royals': 'KCR', 'Seattle Mariners': 'SEA', 'Pittsburgh Pirates': 'PIT',
              'Montreal Expos': 'MON', 'St. Louis Cardinals': 'STL', 'Chicago Cubs': 'CHC', 'New York Mets': 'NYM', 'Philadelphia Phillies': 'PHI', 'Atlanta Braves': 'ATL',
              'Cincinnati Reds': 'CIN', 'San Diego Padres': 'SDP', 'Houston Astros': 'HOU', 'San Francisco Giants': 'SFG', 'Los Angeles Dodgers': 'LAD'}

namesToShorthands = {key: shorthands[key] for key in shorthands.keys()}

def monthFix(x):
    if "Mar" in x: return "3"
    elif "Apr" in x: return "4"
    elif "May" in x: return "5"
    elif "Jun" in x: return "6"
    elif "Jul" in x: return "7"
    elif "Aug" in x: return "8"
    elif "Sep" in x: return "9"
    elif "Oct" in x: return "10"
    else: return "11"

def dayFix(x): return x.split(" ")[2]

def nameFix(x): return namesToShorthands[x]

def tableFix(data):

    data['month'] = data['Date'].apply(monthFix)
    data['day'] = data['Date'].apply(dayFix)
    data['dt'] = pd.to_datetime(str(1992) + '-' + data['month'] + '-' + data['day'])

    return data

def getCurrentRecord(team, date):
    table = tableFix(schedule_and_record(1992, team))

    current_record = table[table['dt'] == pd.to_datetime(date)]

    if current_record.shape[0] < 1:
        current_record = table[table['dt'] < pd.to_datetime(date)]

    current_record = current_record.iloc[current_record.shape[0]-1]['W-L']
    current_record = current_record.split("-")

    return (team, current_record[0], current_record[1])

def getRemainingGames(team, date):

    divisionTeams = getDivision(team, date)

    RemainingGamesTable = pd.DataFrame(columns=divisionTeams)

    year = int(date.split('-')[0])

    for teams in divisionTeams:
        table = tableFix(schedule_and_record(year, teams))
        remainingGames = table[table['dt'] > date]['Opp'].value_counts()
        remainingGames = remainingGames.rename(teams)
        remainingGames[teams] = table[table['dt'] > date].shape[0]
        RemainingGamesTable = RemainingGamesTable.append(remainingGames)

    return RemainingGamesTable

def getDivision(team, date):

    year = date.split('-')[0]
    seasonRecord = standings(int(year))

    for divisions in seasonRecord:
        divisionTeams = list(divisions['Tm'].apply(nameFix))
        if team in divisionTeams:
            break
    return divisionTeams

def getRecords(team, date):

    divisionTeams = getDivision(team, date)

    recordTable = pd.DataFrame([getCurrentRecord(teams, date) for teams in divisionTeams], columns=['Tm', 'W', 'L'])

    return recordTable