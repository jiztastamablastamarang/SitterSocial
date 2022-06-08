import requests
from rest_framework import status
import os
import sys
import json

API_KEY = 'f604bfb58aaa1d0cf75b87fcb18327551ef0cc81'


def email_validation():
    root = '\\'.join(os.path.dirname(__file__).split('\\')[:-3])
    sys.path.append(os.path.join(root, r'sitter\test'))
    config_path = r'sitter\test\config.json'
    path = os.path.join(root, config_path)
    with open(path, 'r') as f:
        data = json.load(f)
    return data['email_validation']


def email_status(email):
    if email_validation():
        request = dict(
            head='https://api.hunter.io/v2/',
            action='email-verifier?email=',
            email=email,
            tail='&api_key=',
            api_key=API_KEY
        )

        r = requests.get(
            url=''.join([value for value in request.values()])
        )
        if r.status_code == status.HTTP_200_OK:
            return r.json()['data']['status']
        else:
            print('error checking email')
    else:
        return 'valid'
