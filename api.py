import requests
from auth import BearerAuth
from auth import get_bearer_token
import auth

access_token = get_bearer_token()

def get_accounts(json=False):
    accounts_response = requests.get('https://web-api.starlink.com/enterprise/v1/accounts/', auth=BearerAuth(access_token))
    if json == True:
        return accounts_response.json()
    else:
        accts = []
        for account in accounts_response.json()['content']['results']:
            accts.append(account['accountNumber'])
        return accts



def get_addresses(account_id):
    addresses_response = requests.get('https://web-api.starlink.com/enterprise/v1/account/' + account_id + '/addresses?limit=50&page=0', auth=BearerAuth(access_token))
    return addresses_response.json()

def get_service_line(account_id, address_id):
    service_line_response = requests.get('https://web-api.starlink.com/enterprise/v1/account/' + account_id + '/address/' + address_id + '/service-line', auth=BearerAuth(access_token))
    return service_line_response.json()