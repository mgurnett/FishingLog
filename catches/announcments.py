from .models import *
# <a href="{% url 'lake_detail' lake.id %}">{{ lake.name | title }}</a>

# Boyle Pond            23
# Cardiff Park Pond     36
# Fort Lions Park Pond  85
# Hermitage Park Pond   103
# Lacombe Park Pond     133
# Lower Chain Lake      151
# Muir Lake             186


lake = Lake.objects.get(id=85)

plan = f'on April 26 at 6pm.  <span style="color:red">Maybe see you there!</span>'

# This can't be blank, or nothing will show up.
# announcment = 'Log in to see the next planned fishing trip' 
# announcment = 'As the site is upgraded it will be documented in blogs' 
announcment = 'Please note that <b>nothing</b> will be saved on this site while it is being upgraded.'

announce = {'type': 'a',
            'plan': plan,
            'lake': lake,
            'announcment': announcment,
            }