from constants import *
import time
import requests
from requests.auth import AuthBase

class Token(AuthBase):
    def __init__(self, access_token):
        self.access_token = access_token
    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.access_token
        return r

class Auth:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = None
        self.token_expiration = 0
    
    def bearer_token(self):
        if time.time() > self.token_expiration:
            url = API_TOKEN_ENDPOINT 
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