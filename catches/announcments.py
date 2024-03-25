from .models import *
import os
import json

with open ('/home/michael/broadcasts.json') as messages_file:
    broadcasts = json.load (messages_file)

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
    'plan': broadcasts ['plan'],
    'lake': Lake.objects.get(id=broadcasts ['id']),
} 

# =====================================
top_messages = {
    'first_slide': first_slide,
    'second_slide': broadcasts ['second_slide'],
    'third_slide': broadcasts ['third_slide'],
}