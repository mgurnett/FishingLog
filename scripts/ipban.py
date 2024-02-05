import requests
import json

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

def run():
    report = json.dumps(check_ip ('165.154.51.243'), sort_keys=True, indent=4)
    print (type(report))