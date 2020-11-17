import requests
import base64
import json
import time

host = 'http://178.159.39.154/'
url_sub = host + '/submissions/batch'
headers = {"X-Auth-Token": "bbb1db97e156ae820590702990b2a469"}


def send_submission(code, expected_output, lang_id):
    data = {'language_id': lang_id,
            'source_code': code,
            'expected_output': expected_output}

    data = {'submissions': [data, data]}
    r = requests.post(url_sub, json=data, headers=headers)
    result = r.json()
    return ','.join(x['token'] for x in result)


def get_results(sub_id):
    params = {'tokens': sub_id}
    r = requests.get(url_sub, params=params, headers=headers)
    return r.json()['status']['description'], r.status_code


python_id = 71
code = """
while True:
    pass
"""
expected_output = """1
3
"""

sub_id = send_submission(code, expected_output, python_id)
time.sleep(2)
print(get_results(sub_id))
