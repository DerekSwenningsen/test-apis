'''
Used to create different authentication headers for APIs
'''

from azure.identity import AzureCliCredential
from azure.identity import ClientSecretCredential


def get_headers():
    '''
    Gets auth token from Azure Cli Credentials and sets minimal headers for
        Sentinel REST API request

    Returns:
        dict: JSON formatted headers for HTTP request
    '''
    token = AzureCliCredential().get_token('https://management.azure.com')
    header_token_value = "Bearer {}".format(token.token)
    headers = {"Authorization": header_token_value,
               "content-type": "application/json"}
    return headers


def get_graph_headers(tenant_id, client_id, client_secret):
    '''
    Gets auth token from Registered App (client_secret and id) and sets
        minimal headers for Sentinel REST API request

    Returns:
        dict: JSON formatted headers for HTTP request
    '''
    # TODO make env variable

    credential = ClientSecretCredential(tenant_id,
                                        client_id,
                                        client_secret)
    scopes = 'https://graph.microsoft.com/.default'
    token = credential.get_token(scopes)
    header_token_value = "Bearer {}".format(token.token)
    headers = {"Authorization": header_token_value,
               "content-type": "application/json"}
    return headers
