import requests
import time
import urllib
import json


class Connection:
    def __init__(self):
        self.headers = None
        self.cookies = None

    def fetch(self, full_url, data=None, method='GET', timeout=60, verify=False):
        if method == 'GET':
            if data is not None:
                url_values = urllib.parse.urlencode(data, encoding='utf-8')
                full_url = full_url + '?' + url_values

            response = requests.get(full_url, headers=self.headers, cookies=self.cookies, timeout=timeout,
                                    verify=verify)
            response.raise_for_status()

        elif method == 'POST':

            response = requests.post(full_url, timeout=timeout, headers=self.headers, cookies=self.cookies,
                                     data=json.dumps(data), verify=verify)
            response.raise_for_status()

        try:
            response = response.json()
        except ValueError:
            response = response.text
        return response
