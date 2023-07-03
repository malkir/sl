import requests
from constants import *
from auth import Auth, Token


auth = Auth(API_CLIENT_ID, API_CLIENT_SECRET) 

def get_accounts(json=False):
    accounts_response = requests.get('https://web-api.starlink.com/enterprise/v1/accounts/', auth=Token(auth.bearer_token()))
    if json == True:
        return accounts_response.json()
    else:
        accts = []
        for account in accounts_response.json()['content']['results']:
            accts.append(account['accountNumber'])
        return accts



def get_addresses(account_id, json=False):
    addresses_response = requests.get('https://web-api.starlink.com/enterprise/v1/account/' + account_id + '/addresses?limit=50&page=0', auth=Token(auth.bearer_token()))
    if json == True:
        return addresses_response.json()
    else:
        addrs = []
        for address in addresses_response.json()['content']['results']:
            addrs.append(address['addressReferenceId'])
        return addrs
    

def get_service_line(account_id, address_id):
    service_line_response = requests.get('https://web-api.starlink.com/enterprise/v1/account/' + account_id + '/address/' + address_id + '/service-line', auth=Token(auth.bearer_token()))
    return service_line_response.json()