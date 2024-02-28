'''
Creates Graph API Client
'''

import requests
from . import api_auth as aa

# Will use when fixed
from . import response_check


class GraphClient:
    '''
    A Class to establish a client to interact with MSFT Graph API Quickly

    Argments
    client_id:string        id of registered app with Graph API perms
    client_secret:string    registered app secret
    auth:string             authority to login
                                (Example: https://login.microsoftonline.com)

    '''
    def __init__(self, tenant_id, client_id, client_secret):
        self.resource = "https://graph.microsoft.com"
        self.api_base = 'https://graph.microsoft.com/v1.0'
        # self.tenant_id = tenant_id
        # self.client_id = client_id
        # self.client_secret = client_secret
        self.headers = aa.get_graph_headers(tenant_id, client_id,
                                            client_secret)

# TODO Fix to remove out and use rc
    def get_inc(self, id, out=False):
        '''
        Pull a particular incident's information from M365 Defender

        Arguments
        id:string           id of incident in M365 Defender
        out:boolean         whether to write output to file
        '''
        incident_endpoint = '/security/incidents/' + id
        request_url = self.api_base + incident_endpoint
        response = requests.get(request_url, headers=self.headers)
        if out:
            with open('graph_inc.json', 'wb') as fd:
                fd.write(response.content)
        return response

# TODO Fix to remove out and use rc
    def get_inc_and_alerts(self, id, out=False):
        '''
        Pull an incident's information and it's alerts information

        Arguments
        id:string           id of incident in M365 Defender
        out:boolean         whether to write output to file
        '''
        incident_endpoint = '/security/incidents/' + id + '?$expand=alerts'
        request_url = self.api_base + incident_endpoint
        response = requests.get(request_url, headers=self.headers)
        if out:
            with open('graph_inc_alerts.json', 'wb') as fd:
                fd.write(response.content)
        return response

# TODO Fix to remove out and use rc
    def update_inc(self, id, body):
        '''
        Update an incident's information

        Arguments
        id:string           id of incident in M365 Defender
        body:json           json formatted body of items to update
                                Example at https://learn.microsoft.com/
                                    en-us/graph/api/security-incident-update
                                    ?view=graph-rest-beta&tabs=http#request-body
        out:boolean         whether to write output to file
        '''
        update_endpoint = '/security/incidents/' + id
        request_url = self.api_base + update_endpoint
        response = requests.patch(request_url, json=body, headers=self.headers)
        return response

# TODO Fix to remove out and use rc
    def get_alert(self, id):
        '''
        Update an incident's information

        Arguments
        id:string           id of incident in M365 Defender
        body:json           json formatted body of items to update
                                Example at https://learn.microsoft.com/
                                    en-us/graph/api/security-incident-update
                                    ?view=graph-rest-beta&tabs=http#request-body
        out:boolean         whether to write output to file
        '''
        update_endpoint = '/security/alerts_v2/' + id
        request_url = self.api_base + update_endpoint
        response = requests.get(request_url, headers=self.headers)
        return response

# TODO Fix to remove out and use rc
    def get_user_photo(self, id, out=False):
        '''
        Pull an incident's information and it's alerts information

        Arguments
        id:string           id of incident in M365 Defender
        out:boolean         whether to write output to file
        '''
        photo_endpoint = '/users/' + id + '/photo/$value'
        request_url = self.api_base + photo_endpoint
        response = requests.get(request_url, headers=self.headers)
        if out:
            with open('graph_inc_alerts.json', 'wb') as fd:
                fd.write(response.content)
        return response
