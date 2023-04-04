from django.shortcuts import render
from django.views.generic.base import TemplateView
import requests
import json
import pandas as pd
from pandas import json_normalize
import numpy as np
from .models import *

from datetime import datetime

URL = "https://statsapi.web.nhl.com/api/v1/"

def get_data (url):
    full_url = f'{URL}{url}'
    # print (f'full_url {full_url}')
    response = requests.get(full_url)
    content = json.loads(response.content)
    return content

class Home(TemplateView):
    template_name = 'nhl/home.html'
    context_object_name = 'teams'

    def get_context_data(self, **kwargs): 
        context = super(Home, self).get_context_data(**kwargs)
        teams_data = get_data ('teams')
        df_team_content = pd.DataFrame(teams_data['teams'])
        context ['teams'] = df_team_content
        # print (df_team_content)
        # print (list(df_team_content))
        return context


class Team(TemplateView):
    template_name = 'nhl/team.html'
    context_object_name = 'teams'
    model = Team


class Person(TemplateView):
    template_name = 'nhl/person.html'
    context_object_name = 'person'

    def get_context_data(self, **kwargs): 
        context = super(Person, self).get_context_data(**kwargs)
        people_data = get_data (f"people/{kwargs['pk']}")
        df_people_content = pd.DataFrame(people_data)
        print (df_people_content)
        print (list(df_people_content))
        context ['people'] = df_people_content
        return context

