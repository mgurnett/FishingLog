import requests
import json
import pandas as pd
from nhl.models import *
import os

from datetime import datetime

URL = "https://statsapi.web.nhl.com/api/v1/"

def get_data (url):
    full_url = f'{URL}{url}'
    # print (f'full_url {full_url}')
    response = requests.get(full_url)
    content = json.loads(response.content)
    return content

def run():
    Team.objects.all().delete()
    team_list = get_data ('teams')
    # print (team_list)
    for team in team_list['teams']:
        # print (f"team name {team['name']} / ID {team['division']['id']}")
        div_pk = Division.objects.get(nhl_id = team['division']['id'])
        # print (div_pk)
        team = Team (
            name = team['name'], 
            nhl_id = team['id'], 
            division = div_pk,
            venue = team['venue']['name'],
            city = team['venue']['city'],
            teamName = team['teamName'],
            locationName = team['locationName'],
              )
        team.save()