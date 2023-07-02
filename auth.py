import requests  
from requests.auth import AuthBase
import constants as c

def get_bearer_token():
    access_token_response = requests.post('https://api.starlink.com/auth/connect/token', data={
        'client_id': c.api_var_client_id,
        'client_secret': c.api_var_client_secret,
        'grant_type': c.api_var_grant_type,
    })
    access_token = access_token_response.json().get('access_token')
    return(access_token)

class BearerAuth(AuthBase):
    def __init__(self, access_token):
        self.access_token = access_token
    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.access_token
        return r



