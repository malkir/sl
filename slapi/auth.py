from .constants import *
from pathlib import Path
from requests.auth import AuthBase
import configparser
import requests
import time

class StarlinkConfig:
    '''
    By default reads:
       ~/.starlink
       [default]
       ClientId = xxx
       ClientSecret = yyy
    '''
    def __init__(self, profile='default'):
        self.config = configparser.ConfigParser()
        self.config.read(Path.home() / '.starlink')
        self.profile = profile

    @property
    def id(self):
        return self.config.get(self.profile, 'ClientId')

    @property
    def secret(self):
        return self.config.get(self.profile, 'ClientSecret')

class Auth:
    def __init__(self, profile='default'):
        client = StarlinkConfig(profile) 
        self.client_id = client.id
        self.client_secret = client.secret
        self.token = None
        self.token_expiration = 0
    
    def bearer_token(self):
        if time.time() > self.token_expiration:
            url = API_AUTH_TOKEN_ENDPOINT 
            data = {
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'grant_type': 'client_credentials',
            }
            response = requests.post(url, data=data)
            response_data = response.json()
            self.token = response_data.get('access_token')
            self.token_expiration = time.time() + ( 14 * 60 ) # 14 minutes
        return self.token


class Token(AuthBase):
    def __init__(self, access_token):
        self.access_token = access_token
    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.access_token
        return r
