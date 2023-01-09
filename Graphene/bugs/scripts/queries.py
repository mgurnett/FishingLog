from insects.models import *

def run():
    # temps = Temp.objects.all()

    # for t in temps:
    #     print (t)

    # for hatch in Hatch.objects.filter(bug__name = "Chironomids"):
    #     print (hatch.bug.name)  #works

    # Chironomids

    # for bug in Bug.objects.all():
    #     print (bug.insect.bug.name)  

    # for hatch in Hatch.objects.all():
    #     print (hatch.bug.name)

    # Caddisflies


    # for stength in Strength.objects.all():
    #     print (stength.hatch.bug.name)

    # for stength in Strength.objects.all():
    #     print (stength.week.number)

    # for stength in Strength.objects.filter(week__number = 44):
    #     print (stength)
    '''
    bug: Shrimp in week: 44 has a strength of: 5
    bug: Zooplankton  Daphnia in week: 44 has a strength of: 3
    bug: Leeches in week: 44 has a strength of: 4
    bug: Water Boatman  Backswimmer in week: 44 has a strength of: 3
    bug: Chironomids in week: 44 has a strength of: 1
    bug: Mayflys in week: 44 has a strength of: 1
    bug: Damselflies in week: 44 has a strength of: 3
    bug: Dragon Flies in week: 44 has a strength of: 1
    bug: Caddisflies in week: 44 has a strength of: 1
    '''

    # for stength in Strength.objects.filter(week__number = 44):
    #     print (stength.hatch.bug)

    '''bug = Bug.objects.get(name = "Mayflys")
    print (bug)    #Mayflys
    bug = Bug.objects.get(name__contains = "Mayfly")
    print (bug)    #Mayflys
    print (bug.id)    #10
    print (bug.insect.all()) #worked  Found all hatches with Mayflies.'''

    # Find the strength of the Mayfly during week 30
    bug = Bug.objects.get(name__contains = "Mayfly")
    week = Week.objects.get(number=30)
    # print (week.id)  # > 93
    hatch = Hatch.objects.get(week=week.id, bug=bug.id)
    # for hatch in hatches:
    # print (f'{hatch} {week.number}')   #-> Mayflys are often found during the weeks of  30

    # strength = Strength.objects.get(week=week.id, hatch=hatch.id)
    # print (strength.strength)   # -> bug: Mayflys in week: 30 has a strength of: 3

    # hatch_strength = Hatch.objects.get(id=hatch.strength_of_hatch)
    # print (hatch.strength_of_hatch.first().strength)

    print (f'During the week of {week.number}, the {bug.name} has a strength of {hatch.strength_of_hatch.first().strength}') 
    #  ->  During the week of 30, the Mayflys has a strength of 3