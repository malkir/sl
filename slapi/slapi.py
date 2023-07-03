import requests
from .constants import *
from .auth import Auth, Token

'''
You must have a ~/.starlink file, please see auth.py
'''
auth = Auth() 

def get_accounts(limit=50, page=0, regioncode=None, json=False):
    region = f'&regionCode={regioncode}' if regioncode else ''
    accounts_response = requests.get(f'{API_ACCOUNTS_ENDPOINT}?limit={limit}&page={page}{region}', auth=Token(auth.bearer_token()))
    if json == True:
        return accounts_response.json()
    else:
        accts = []
        for account in accounts_response.json()['content']['results']:
            accts.append(account['accountNumber'])
        return accts


def get_addresses(account_id, limit=50, page=0, json=False):
    '''
    Todo: add address ID filter
    '''
    addresses_response = requests.get(f'{API_ACCOUNT_ENDPOINT}/{account_id}/addresses?limit={limit}&page={page}', auth=Token(auth.bearer_token())) # Todo: shoddy way of handling the endpoint name by appending
    if json == True:
        return addresses_response.json()
    else:
        addrs = []
        for address in addresses_response.json()['content']['results']:
            addrs.append(address['addressReferenceId'])
        return addrs
    

def get_service_line(account_id, address_id, limit=50, page=0, descending=True, json=False):
    service_line_response = requests.get(f'{API_ACCOUNT_ENDPOINT}/{account_id}/service-lines?limit={limit}&page={page}&orderByCreatedDateDescending={descending}', auth=Token(auth.bearer_token()))
    return service_line_response
    #print(service_line_response)
    #return service_line_response.json()