from .models import *

# =====================================
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
first_slide = {
    'plan': plan,
    'lake': lake,
} 

# =====================================
# announcment = 'Log in to see the next planned fishing trip' 
# announcment = 'As the site is upgraded it will be documented in blogs' 
second_slide = 'Please note that <b>nothing</b> will be saved on this site while it is being upgraded.'

# =====================================
third_slide = 'The live version will launch <b>April 1, 2024</b>'



# =====================================
top_messages = {
    'first_slide': first_slide,
    'second_slide': second_slide,
    'third_slide': third_slide,
}

# <b>{{ first_slide.lake.name | title }}</b>{{ first_slide.plan | safe }}
# <a href="{% url 'lake_detail' first_slide.lake.id %}"</a> 