from insects.models import *
import os
import sqlite3
from sqlite3 import Error
import csv

def fill_weeks():
    for week_num in range(15, 49):
        the_week = Week (number = week_num)
        print (str(week_num) + '    ' + str(the_week.number))
        # the_week.save()

def get_csv (file_name):
    with open(file_name) as file:
        reader = csv.reader(file)
        next(reader)  # Advance past the header
        csv_data = []
        for r in reader:
            csv_data.append(r)
    return csv_data


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

# pd.read_csv(filename).to_sql(tablename, con)


    database = r"db.sqlite3"

    # create a database connection
    conn = create_connection(database)



def run():
    fill_weeks
    csv_file = get_csv ('scripts/hatch_chart.csv')
    bug_list = []
    for line in csv_file:
        bug = Bug.objects.filter(name = line[0])
        if bug:
            for b in bug:
                # print (f'Name found is: {line[0]} and bug name is: {b.name}')
                bug_list.append ([b.id, b.name])
    print (bug_list)


