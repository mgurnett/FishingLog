import requests
import json
import csv
import sqlite3
from sqlite3 import Error

def check_ip (ipAddress):

    # Defining the api-endpoint
    url = 'https://api.abuseipdb.com/api/v2/check'

    querystring = {
        'ipAddress': ipAddress,
        'maxAgeInDays': '90'
    }

    headers = {
        'Accept': 'application/json',
        'Key': 'd7d173c9ab1284385c42bb87fb42cba58167aa7fecc6855175f8bef06bf5414e2d1fa3511e90e884'
    }

    response = requests.request(method='GET', url=url, headers=headers, params=querystring)

    # Formatted output
    return json.loads(response.text)

def get_csv_data ():
    with open('request event.csv') as csvfile:
        rows_full= csv.reader(csvfile, delimiter=',')
        ip_list = []
        for row in rows_full:
            if not row[4]: # if not a user
                ip_list.append (row[5])
        
        # print (f'{ip_list=} length is {len(ip_list)}')
        ip_list = list(dict.fromkeys(ip_list))
        # print (f'{ip_list=} length is {len(ip_list)}')

        ip_list_sorted = sorted(ip_list)
        # print (f'{ip_list_sorted=} length is {len(ip_list)}')
    return ip_list_sorted

def get_ips():
    conn = None
    try:
        conn = sqlite3.connect('db.sqlite3')
    except Error as e:
        print(e)

    cur = conn.cursor()
    cur.execute("SELECT * FROM easyaudit_requestevent")

    rows = cur.fetchall()
    ip_list = []
    for row in rows:
        if not row[5]: # if not a user
            ip_list.append (row[4])
    
    print (f'{ip_list=} length is {len(ip_list)}')
    ip_list = list(dict.fromkeys(ip_list))
    # print (f'{ip_list=} length is {len(ip_list)}')

    ip_list_sorted = sorted(ip_list)
    print (f'{ip_list_sorted=} length is {len(ip_list)}')
    return ip_list_sorted

def check_ip_list (ip_list_sorted):
    list_of_ip = []
    for ip in ip_list_sorted:
        report = check_ip (ip)
        score = report['data']['abuseConfidenceScore']
        if score > 0:
            result = {'ip': ip, 'score': score}
            list_of_ip.append (result)
    return (list_of_ip)
    

def run():
    # report = json.dumps(check_ip ('165.154.51.243'), sort_keys=True, indent=4)
    # print (report)
    # report = check_ip ('66.249.66.36')
    # result = report['data']['abuseConfidenceScore']
    # print (result)

    # ip_list_sorted = get_csv_data ()   # get the data from CSV

    ip_list_sorted = get_ips()   # get the data directly from the database
    # for q in ip_list_sorted:  # Test
    #     print (f'{q = }')

    list_of_ip = check_ip_list (ip_list_sorted)
    print (f'{list_of_ip=}')