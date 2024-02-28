import base64
import requests
from enum import Enum

"""
Script to connect to ps3838 API
URL to check API User Guide:
https://www.tender88.com/static/index.php/es-es/help/api-user-guide-es-es
In order to access PS3838 API you must have a funded account.
"""

# API ENDPOINT
API_ENDPOINT = 'http://api.ps3838.com'


# Available Request Methods
class HttpMethod(Enum):
    GET = 'GET'
    POST = 'POST'


# Constants to fill by each user
PS3838_USERNAME = "FILL_USERNAME_HERE"
PS3838_PASSWORD = "FILL_PASSWORD_HERE"


def get_headers(request_method: HttpMethod) -> dict:
    headers = {}
    headers.update({'Accept': 'application/json'})
    if request_method is HttpMethod.POST:
        headers.update({'Content-Type': 'application/json'})

    headers.update({'Authorization': 'Basic {}'.format(
        base64.b64encode((bytes("{}:{}".format(PS3838_USERNAME, PS3838_PASSWORD), 'utf-8'))).decode())
    })

    return headers


def get_operation_endpoint(operation: str) -> str:
    return '{}{}'.format(API_ENDPOINT, operation)


def get_sports():
    operation = '/v1/sports'
    req = requests.get(
        get_operation_endpoint(operation),
        headers=get_headers(HttpMethod.GET)
    )
    return req.json()


# Test retrieve sports endpoint
print(get_sports())