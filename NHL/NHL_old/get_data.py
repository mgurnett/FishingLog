import requests
import json
import pandas as pd
import numpy as np

from datetime import datetime

teams_url = "https://statsapi.web.nhl.com/api/v1/teams"

team_response = requests.get(teams_url)

# convert the content into a python dictionary
team_content = json.loads(team_response.content)
# type(team_content)

# team_content.keys()
# print (team_content.keys())

# print (team_content['teams'][22])
# for team in team_content['teams']:
#     print (team)

team_response.json() == json.loads(team_response.content)


df_team_content = pd.DataFrame(team_content['teams'])
df_team_content.head()
# print (df_team_content)

df_team_content2 = df_team_content.convert_dtypes()
# print (df_team_content2.info())

# print (df_team_content2.query("teamName == 'Oilers'"))

df_team_content_jn = pd.json_normalize(team_content['teams'])
# print (df_team_content_jn.info())

df_team_content = df_team_content_jn
print (df_team_content)


teams_url = "https://statsapi.web.nhl.com/api/v1/teams"
team_response = requests.get(teams_url)

team_content = json.loads(team_response.content)
df_teams = pd.json_normalize(team_content['teams'],
sep = "_")

df_teams.info()

df_teams['link'] = 'https://statsapi.web.nhl.com' + df_teams['link']
df_active = df_teams.loc[df_teams['active']==True]

def get_team_roster(team, season):

    base_url = df_active.loc[df_active['name']==team]['link'].iloc[0]
    print(base_url)
    url = base_url + "/roster/" + "?season=" + season
    
    response = requests.get(url)
    roster = response.json()["roster"]
    
    df_roster = pd.json_normalize(roster, sep = "_").astype(str)

    return df_roster
    
df_roster = get_team_roster("Edmonton Oilers", '20222023')

print (df_roster)

def get_career_stats(player_id):

      
    url = 'https://statsapi.web.nhl.com/api/v1/people/' + player_id + '/stats/?stats=yearByYear'
    response = requests.get(url)
    content = json.loads(response.content)['stats']
    splits = content[0]['splits']

    df_splits = (pd.json_normalize(splits, sep = "_" )
             .query('league_name == "National Hockey League"')
            )
    if df_splits.shape[0] > 0 :
    
        url_info = 'https://statsapi.web.nhl.com/api/v1/people/' + player_id
        response = requests.get(url_info)
        player_info = json.loads(response.content)['people'][0]

        if player_info['primaryPosition']['code'] != "G":
            df_splits['goals_per_game']=  df_splits['stat_goals']/df_splits['stat_games']
        df_splits['player_id'] = player_id
        df_splits['first_name'] = player_info['firstName']
        df_splits['last_name'] = player_info['lastName']
        df_splits['bday'] = pd.to_datetime(player_info['birthDate'])
        df_splits['season_end_yr'] = [x[4:8] for x in df_splits['season']]
        df_splits['season_start_yr'] = [x[0:4] for x in df_splits['season']]
        df_splits['season_start_dt'] =  [datetime.strptime(x + '0930', "%Y%m%d") for x in df_splits['season_start_yr']] 
        df_splits['age'] = (np.floor((df_splits['season_start_dt'] - df_splits['bday'])/ np.timedelta64(1,'Y') ))
        df_splits['age'] = df_splits['age'].astype(int)
    
    return df_splits
    
print (get_career_stats(player_id = '8478402'))