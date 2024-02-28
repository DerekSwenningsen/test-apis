from . import messages
import requests
from . import api_auth as aa
from . import response_check


class MonitorClient:
    '''
    A Class to establish a client to interact with Monitor REST API

    Argments
    client_id:string        id of registered app with Graph API perms
    client_secret:string    registered app secret
    sub:string              subscription id
    rg:string               resource group name
    ws:string               workspace name
    auth:string             authority to login
                                (Example: https://login.microsoftonline.com)

    '''
    def __init__(self, sub, rg, api_version):
        """
         Initialize the Azure Management REST API.
            Subclasses should override this if they need to customize the
            resource and headers

         Args:
            sub: The subscription Id to use for the resource
            rg: The resource group name to use for the resource.
            api_version: The API version to use for the
        """
        self.sub = sub
        self.rg = rg
        self.resource = "https://management.azure.com"
        self.api_base = 'https://management.azure.com/subscriptions/' + \
            self.sub + '/resourceGroups/' + self.rg + \
            '/providers/Microsoft.Insights/'
        self.headers = aa.get_headers()
        self.api_version = f'?api-version={api_version}'

    def get_dcr(self, name):
        """
         Gets Data Collection Rule. Rule is returned or False if error.

         Args:
            name: ( str ) Name of DCR. Case insensitive.

         Returns:
            ( dict ) Dictionary rep of JSON response or False if error occured
                during request. Example usage. >>> client. get_dcr ('name')
                Traceback ( most recent call last ) : Exception
        """
        resource = f'dataCollectionRules/{name}'
        url = self.api_base + resource + self.api_version
        response = requests.get(url, headers=self.headers, verify=True)
        # Return the DCR if successful else False.
        if response_check.response_check(response):
            messages.success(f'Successfully retreived DCR: {name}')
            return response.json()
        else:
            return False

    def create_dcr(self, name: str, body: dict) -> dict:
        """
         Create a Data Collection Rule from a predefined body.
            This is a convenience method for creating a dataCollectionRule
                with a predefined body

         Args:
            name: Name of new DCR to create
            body: Dictionary rep of JSON body for DCR creation

         Returns:
            Response from API or False if error ( response code! = 200 ) or
                OK ( response code == 200 )
        """
        resource = f'dataCollectionRules/{name}'
        url = self.api_base + resource + self.api_version
        response = requests.put(url, headers=self.headers, verify=True,
                                json=body)
        # Return the DCR object if successful.
        if response_check.response_check(response):
            messages.success(f'Successfully created DCR: {name}')
            return response.json()
        else:
            return False

    def create_table(self, table_name: str, ws_name: str, body: dict) -> dict:
        """
         Create a table in a log analytics workspace from a predefined body.
            This is a convenience method for creating a dataCollectionRule
                with a predefined body

         Args:
            table_name: Name of new table to create
            ws_name: Name of workspace
            body: Dictionary rep of JSON body for table creation

         Returns:
            Response from API or False if error ( response code! = 200 ) or
                OK ( response code == 200 )
        """
        resource = f'{ws_name}/tables/{table_name}'
        api_base = 'https://management.azure.com/subscriptions/' + \
            self.sub + '/resourceGroups/' + self.rg + \
            '/providers/Microsoft.OperationalInsights/workspaces/'
        url = api_base + resource + self.api_version
        response = requests.put(url, headers=self.headers, verify=True,
                                json=body)
        if response_check.response_check(response):
            if response.status_code == 202:
                messages.success(f'Creating DCR: {table_name}. Verify in WS')
                return response
            else:
                messages.success(f'Successfully created DCR: {table_name}')
                return response.json()
        else:
            return False
