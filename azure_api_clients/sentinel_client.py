'''
Creates Sentinel API Client
'''

import requests
from . import api_auth
from . import messages
from . import response_check


class SentinelClient:
    '''
    A Class to establish a client to interact with MSFT Sentinel REST API

    Argments
    sub:string              subscription id
    rg:string               resource group name
    ws:string               workspace name
    '''
    def __init__(self, sub, rg, ws, api_version):
        """
         A Class to establish a client to interact with MSFT Sentinel REST API.

         Args:
            sub: The id of the subscription to use
            rg: The resource group name to use ( REQUIRED ).
            ws: The workspace name to use ( REQUIRED ).
            api_version
        """
        self.sub = sub
        self.rg = rg
        self.ws = ws
        self.resource = "https://management.azure.com"
        self.api_base = 'https://management.azure.com/subscriptions/' + \
            self.sub + '/resourceGroups/' + self.rg + \
            '/providers/Microsoft.OperationalInsights/workspaces/' + self.ws +\
            '/providers/Microsoft.SecurityInsights/'
        self.headers = api_auth.get_headers()
        self.api_version = f'?api-version={api_version}'

    def get_inc(self, id):
        """
         Get an incident's information from Sentinel

         Args:
            id: id of the incident to retrieve

         Returns:
            dict of incident information or False if not found or error while
                getting incident information from Sentinel
        """
        incident_endpoint = 'incidents/'
        request_url = self.api_base + incident_endpoint + id + self.api_version
        response = requests.get(request_url, headers=self.headers)
        # Return the incident data.
        if response_check.response_check(response):
            messages.success(f'Successfully got incident: {id}')
            return response.json()
        else:
            return False

    def get_alert(self, id):
        """
         Get information about an incident's alert from Sentinel

         Args:
            id: incident's unique identifier

         Returns:
            dict with information about the incident's alert or False if not
                found or error while communicating
        """
        incident_endpoint = 'incidents/' + id + '/alerts' + self.api_version
        request_url = self.api_base + incident_endpoint
        response = requests.post(request_url, headers=self.headers)
        # Return the alert if successful False otherwise.
        if response_check.response_check(response):
            success(f'Successfully got alert: {id}')
            return response.json()
        else:
            return False

# TODO Fix to remove out and use rc
    def create_inc(self, id, body, out=False):
        """
         Create Incident in Sentinel by id and return response object.

         Args:
            id: incident id to be created
            body: json body of items to update in the incident
            out: boolean whether to write output to file default False

         Returns:
            response object from requests library or json if out = True
                response object will be returned in json format if out
        """
        incident_endpoint = 'incidents/' + id + self.api_version
        request_url = self.api_base + incident_endpoint
        response = requests.put(request_url, json=body, headers=self.headers)
        # If out is true write the sent inc alert. json to file
        if out:
            with open('sent_inc_alert.json', 'wb') as fd:
                fd.write(response.content)

        return response

# TODO Fix to remove out and use rc
    def purge_data(self, body, out=False):
        """
         Purge Incident data from Sentinel.
            Purge data is a way to get a list of incident's data
            by sending a POST request to the purge endpoint.

         Args:
            body: json formatted body of items to update
            out: boolean whether to write output to file default is False

         Returns:
            requests response object from API and data to be used in other
                methods of this class. Example response object is
                returned as JSON
        """
        purge_endpoint = '/purge?api-version=2020-08-01'
        base_url = 'https://management.azure.com/subscriptions/' + \
            self.sub + '/resourceGroups/' + self.rg + \
            '/providers/Microsoft.OperationalInsights/workspaces/' + self.ws
        request_url = base_url + purge_endpoint
        response = requests.post(request_url, json=body, headers=self.headers)
        # purge the response from the server
        if out:
            with open('purge_response.json', 'wb') as fd:
                fd.write(response.content)

        return response

# TODO Fix to remove out and use rc
    def get_alert_ruleTemplates(self, out=False):
        """
        Get list of alert rule templates.

        Args:
            out: Output file to write to

        Returns:
            HTTP response from API ( json ) or None
            if not succesful ( error )
        """

        incident_endpoint = 'alertRuleTemplates/' + self.api_version
        request_url = self.api_base + incident_endpoint
        response = requests.get(request_url, headers=self.headers)
        # Write the sent alert rule templates to json file
        if out:
            with open('sent_alert_ruleTemplates.json', 'wb') as fd:
                fd.write(response.content)

        return response

# TODO Fix to remove out and use rc
    def get_alert_ruleTemplate(self, id, out=False):
        """
        Get alert rule template by id.

        Args:
            id: id of the alert rule template
            out: if True the response will be written to
                sent_alert_ruleTemplate. json

        Returns:
            json object of the alert rule template that was passed as
                parameter or
                None if not found or error while querying
        """

        alert_template_endpoint = 'alertRuleTemplates/' + id + self.api_version
        request_url = self.api_base + alert_template_endpoint
        response = requests.get(request_url, headers=self.headers)
        # Write the sent alert rule template to json file
        if out:
            with open('sent_alert_ruleTemplate.json', 'wb') as fd:
                fd.write(response.content)

        return response.json()

# TODO Fix to remove out and use rc
    def get_alertrules(self, out=False):
        """
        Get alert rules from Alert

        Args:
            out: If True write the response to sent_alert_ruless. json

        Returns:
            response from API call as a requests. Response object or None if
                there was an error.
        """

        alert_endpoint = 'alertRules' + self.api_version
        request_url = self.api_base + alert_endpoint
        response = requests.get(request_url, headers=self.headers)
        # If out is true write rule to json file
        if out:
            with open('sent_alert_ruless.json', 'wb') as fd:
                fd.write(response.content)

        return response

# TODO Fix to remove out and use rc
    def get_product_templates(self, out=False):
        """
         Get all templates in the catalog.

         Args:
            out: ( optional ) return output instead of reading it from the API

         Returns:
            Dictionary with template information.
        """
        prod_endpoint = 'contentProductTemplates' + self.api_version
        request_url = self.api_base + prod_endpoint

        return requests.get(request_url, headers=self.headers).json()

# TODO Fix to remove out and use rc
    def get_data_conns(self, out=False):
        """
        Get alert rules from Alert

        Args:
            out: If True write the response to sent_alert_ruless. json

        Returns:
            response from API call as a requests. Response object or None if
                there was an error.
        """

        alert_endpoint = 'dataConnectors' + self.api_version
        request_url = self.api_base + alert_endpoint
        response = requests.get(request_url, headers=self.headers)
        # If out is true write rule to json file
        if out:
            with open('sent_alert_ruless.json', 'wb') as fd:
                fd.write(response.content)
        if response_check.response_check(response):
            return response.json()

    def run_query(self, ws_id, query, out=False):
        """
        Get alert rules from Alert

        Args:
            out: If True write the response to sent_alert_ruless. json

        Returns:
            response from API call as a requests. Response object or None if
                there was an error.
        """

        alert_endpoint = 'dataSources' + self.api_version
        base = f'https://api.loganalytics.io/v1/workspaces/{ws_id}/query'
        request_url = base + alert_endpoint
        response = requests.post(request_url, headers=self.headers, json=query)
        # If out is true write rule to json file
        if out:
            with open('sent_alert_ruless.json', 'wb') as fd:
                fd.write(response.content)
        if response_check.response_check(response):
            return response.json()
