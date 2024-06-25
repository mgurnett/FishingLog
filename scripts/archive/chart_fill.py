from catches.models import *
import os
import csv

def fill_weeks():
    Week.objects.all().delete()
    for week_num in range(14, 49):
        the_week = Week (number = week_num)
        # print (str(week_num) + '    ' + str(the_week.number))
        the_week.save()
    return ()

def get_csv (file_name):
    with open(file_name) as file:
        reader = csv.reader(file)
        next(reader)  # Advance past the header
        csv_data = []
        for r in reader:
            csv_data.append(r)
    return csv_data

def get_bug_list(csvfile):
    bug_list = []
    for line in csvfile:
        first_word = line[0].split()[0]
        # print (line[0] + first_word)
        bug = Bug.objects.filter(name__contains = first_word)
        if bug:
            for b in bug:
                # print (f'Name found is: {line[0]} and bug name is: {b.name}')
                bug_list.append ([b.id, b.name])
    return bug_list

def get_bug_id(line):
    bug_id = 0
    first_word = line[0].split()[0]
    print (line[0] + first_word)
    bug = Bug.objects.filter(name__contains = first_word)
    if bug:
        for b in bug:
            # print (f'Name found is: {line[0]} and bug name is: {b.name}')
            bug_id = [b.id]
    print (bug_id)
    return bug_id

def run():
    # fill_weeks()
    # Hatch.objects.all().delete()
    Chart.objects.all().delete()
    csv_file = get_csv ('scripts/hatch_chart.csv')
    for row in csv_file:
        bug_id = get_bug_id (row)[0]
        b = Bug.objects.get(id=bug_id)
        print (f'We looked for bug: {b} the name of the bug found in the csv file and it is ID in the Bug database {bug_id}')

        for x in range(1, 36):
            w = Week.objects.get( number = (x + 13) )

            c = Chart ( bug = b, week = w, strength = row[x] )
            c.save()

            print (f'row is: {row}')
            print (f'# {x} week is {w.number}, hatch is {c} and strength is {row[x]}')

