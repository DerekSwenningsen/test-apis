'''
    Checks requests for error code
'''

from . import messages


def response_check(response):
    """
     Check HTTP response for errors.

     Args:
        response: response from requests package
    """
    if response.status_code > 399:
        messages.error(f'{response.status_code}')
        r = response.json()
        messages.error(f'{r["error"]}')
        return False
    else:
        return True
