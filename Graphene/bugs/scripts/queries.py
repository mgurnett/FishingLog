from insects.models import *

def run():
    temps = Temp.objects.all()

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

    bug = Bug.objects.get(name = "Mayflys")
    print (bug)    #Mayflys
    bug = Bug.objects.get(name__contains = "Mayfly")
    print (bug)    #Mayflys
    print (bug.id)    #10
    print (bug.hatch_set.all())