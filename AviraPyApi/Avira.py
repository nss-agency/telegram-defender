import requests
import json


class Avira:
    api_key = ''
    url = ''

    def __init__(self, api_key='', url=''):
        self.api_key = api_key
        self.url = url

    def scan_url(self, urls: list):
        result = {}
        response = requests.request("POST", self.url, headers={
            'X-API-KEY': self.api_key,
            'Content-Type': "application/json",
            'Accept': 'application/json',
        }, data=json.dumps({'urls': urls}))

        result['status_code'] = response.status_code
        result['scans'] = list()
        json_data = json.loads(response.text)
        if response.status_code == 200:
            for num, u in enumerate(urls, 0):
                result['scans'].append({'url': u, 'category': json_data['res'][num]['cat'][0]}) #TODO: Message
        else:
            result['message'] = json_data['msg']

        return result