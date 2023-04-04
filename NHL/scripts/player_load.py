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
    Player.objects.all().delete()
    team_list = Team.objects.all()
    for team in team_list:
        print (team)
        roster = get_data (f'teams/{team.nhl_id}/roster')
        # print (roster)
        for player in roster['roster']:
            nhl_id = player['person']['id']
            # print (f"{player['person']['fullName']} {player['jerseyNumber']}")
            player_detail = get_data (f'people/{nhl_id}')
            team_pk = Team.objects.get(nhl_id = player_detail['people'][0]['currentTeam']['id'])
            player_info = Player(
                firstName = player_detail['people'][0]['firstName'],
                lastName = player_detail['people'][0]['lastName'],
                nhl_id = nhl_id,
                jersey = player['jerseyNumber'],
                birthDate = player_detail['people'][0]['birthDate'],
                nationality = player_detail['people'][0]['nationality'],
                height = player_detail['people'][0]['height'],
                weight = player_detail['people'][0]['weight'],
                active = player_detail['people'][0]['active'],
                alternateCaptain = player_detail['people'][0]['alternateCaptain'],
                captain = player_detail['people'][0]['captain'],
                rookie = player_detail['people'][0]['rookie'],
                shootsCatches = player_detail['people'][0]['shootsCatches'],
                rosterStatus = player_detail['people'][0]['rosterStatus'],
                team = team_pk,
                primaryPosition = player_detail['people'][0]['primaryPosition']['code'],
            )

            player_info.save()


