from .models import *
import os
import json

with open ('/home/michael/messages.json') as messages_file:
    messages = json.load (messages_file)

# =====================================
# This is changed in /home/michael/messages.json

# Boyle Pond            23
# Cardiff Park Pond     36
# Fort Lions Park Pond  85
# Hermitage Park Pond   103
# Lacombe Park Pond     133
# Lower Chain Lake      151
# Muir Lake             186

first_slide = {
    'plan': messages ['plan'],
    'lake': Lake.objects.get(id=messages ['id']),
} 

# =====================================
top_messages = {
    'first_slide': first_slide,
    'second_slide': messages ['second_slide'],
    'third_slide': messages ['third_slide'],
}