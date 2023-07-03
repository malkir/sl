import requests
from .constants import *
from .auth import Auth, Token
from .geo import ReverseGeo

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


def get_addresses(account_id, metadata=None, limit=50, page=0, json=False):
    '''
    Todo: add address ID filter
    '''
    addresses_response = requests.get(f'{API_ACCOUNT_ENDPOINT}/{account_id}/addresses?limit={limit}&page={page}', auth=Token(auth.bearer_token())) # Todo: shoddy way of handling the endpoint name by appending
    if json == True:
        return addresses_response.json()
    else:
        addrs = []
        for address in addresses_response.json()['content']['results']:
            if metadata:
                if address['metadata'] == metadata:
                    return([address['addressReferenceId']])
            addrs.append(address['addressReferenceId'])
        return addrs

def add_address(account_id, lat, lon, metadata=None, json=False):
    geo = ReverseGeo()
    address = geo.reverse_geocode(lat, lon, metadata=metadata)
    headers = {'Content-Type': 'application/json'}
    print(address)
    add_address_response = requests.post(f'{API_ACCOUNT_ENDPOINT}/{account_id}/addresses', auth=Token(auth.bearer_token()), 
                                        data=address, headers=headers)
    if json == True:
        return add_address_response.json()
    else:
        return add_address_response.status_code

def delete_address(account_id, address_id=None, metadata=None, json=False):
    if not address_id or metadata:
        return 'You must specify an address ID or metadata'
    if metadata:
        address_id = get_addresses(account_id, metadata=metadata)[0]
    if address_id:
        delete_address_response = requests.delete(f'{API_ACCOUNT_ENDPOINT}/{account_id}/addresses/{address_id}', auth=Token(auth.bearer_token()))
        if json == True:
            return delete_address_response.json()
        else:
            return delete_address_response.status_code

def get_service_line(account_id, limit=50, page=0, descending=True, json=False):
    service_line_response = requests.get(f'{API_ACCOUNT_ENDPOINT}/{account_id}/service-lines?limit={limit}&page={page}&orderByCreatedDateDescending={descending}', auth=Token(auth.bearer_token()))
    if json == True:
        return service_line_response.json()
    else:
        service_lines = []
        for service_line in service_line_response.json()['content']['results']:
            service_lines.append(service_line['serviceLineNumber'])
        return service_lines

def get_user_terminals(account_id, limit=50, page=0, json=False):
    user_terminals_response = requests.get(f'{API_ACCOUNT_ENDPOINT}/{account_id}/user-terminals?limit={limit}&page={page}', auth=Token(auth.bearer_token()))
    if json == True:
        return user_terminals_response.json()
    else:
        user_terminals = []
        for user_terminal in user_terminals_response.json()['content']['results']:
            user_terminals.append(user_terminal['userTerminalId'])
        return user_terminals

def remove_user_terminal_from_service_line(account_id, user_terminal_id, service_line_id, json=False):
    remove_user_terminal_response = requests.delete(f'{API_ACCOUNT_ENDPOINT}/{account_id}/user-terminals/{user_terminal_id}/{service_line_id}', auth=Token(auth.bearer_token()))
    if json == True:
        return remove_user_terminal_response.json()
    else:
        return remove_user_terminal_response.status_code

def add_user_terminal_to_service_line(account_id, user_terminal_id, service_line_id, json=False):
    add_user_terminal_response = requests.post(f'{API_ACCOUNT_ENDPOINT}/{account_id}/user-terminals/{user_terminal_id}/{service_line_id}', auth=Token(auth.bearer_token()))
    if json == True:
        return add_user_terminal_response.json()
    else:
        return add_user_terminal_response.status_code