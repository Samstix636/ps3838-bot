import base64
import requests
from enum import Enum
from pprint import pprint

# API ENDPOINT
API_ENDPOINT = 'https://api.ps3838.com'


# Available Request Methods
class HttpMethod(Enum):
    GET = 'GET'
    POST = 'POST'


# Constants to fill by each user
PS3838_USERNAME = "BIA0003Q91"
PS3838_PASSWORD = "Iowahawkeyes1@"


def get_headers(request_method: HttpMethod) -> dict:
    headers = {}
    headers.update({'Accept': 'application/json'})
    if request_method is HttpMethod.POST:
        headers.update({'Content-Type': 'application/json'})

    headers.update({'Authorization': 'Basic {}'.format(
        base64.b64encode((bytes("{}:{}".format(PS3838_USERNAME, PS3838_PASSWORD), 'utf-8'))).decode()),
                    'Accept': 'application/json',
                    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    })

    return headers


def get_operation_endpoint(operation: str) -> str:
    return '{}{}'.format(API_ENDPOINT, operation)


def get_sports():
    operation = '/v3/sports'
    req = requests.get(
        get_operation_endpoint(operation),
        headers=get_headers(HttpMethod.GET)
    )
    return req.json()

def get_balance():
    operation = '/v2/client/balance'
    req = requests.get(
        get_operation_endpoint(operation),
        headers=get_headers(HttpMethod.GET)
    )
    return req.json()


def get_period():
    operation = '/v1/periods'
    req = requests.get(
        get_operation_endpoint(operation),
        headers=get_headers(HttpMethod.GET),
        params= {'sportId': 29}
    )
    return req.json()


# Test retrieve sports endpoint
# pprint(get_sports())
pprint(get_period())


def parse_bet_type(info):
    if info == 'S':
        bet_type = 'SPREAD'
    elif info == 'T':
        bet_type = 'TOTAL_POINTS'
    elif info == 'M':
        bet_type = 'MONEYLINE'
    elif info == 'I':
        bet_type = 'TEAM_TOTAL_POINTS'
    else:
        bet_type = None
    return bet_type

def parse_team(id):
    if id == '0':
        team = 'TEAM1'
    elif id == '1':
        team = 'TEAM2'
    elif id == '2':
        team = 'DRAW'
    
    return team

def parse_side(id):
    if id == '0':
        side = 'OVER'
    elif id == '1':
        side = 'UNDER'

def parse_bet_info(bet_info):
    # 1586333564/2426942860||I|0/0/3/0/1.763?line=0.5
    bet_link = bet_info['direct_link']
    line = bet_info['market_and_bet_type_param']
    
    bet_data = {}
    bet_link = bet_link.replace('/', '|')
    data = bet_link.split('|')
    bet_data['event_id'] = data[0]
    bet_data['line_id'] = data[1]
    bet_type = parse_bet_type(data[3])
    bet_data['bet_type'] = bet_type
    bet_data['period_id'] = data[4]
    if bet_type == 'MONEYLINE':
        bet_data['handicap'] = None
        bet_data['side'] = None
        bet_data['team'] = parse_team(data[5])
    elif bet_type == 'TOTAL POINTS':
        bet_data['handicap'] = line
        bet_data['side'] = None
        bet_data['team'] = parse_team(data[5])
        
    
    
    


    
        