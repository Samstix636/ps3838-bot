import base64
import requests
from enum import Enum
from pprint import pprint
import json
from time import sleep
from uuid import uuid4

# API ENDPOINT
API_ENDPOINT = 'https://api.ps3838.com'


# Available Request Methods
class HttpMethod(Enum):
    GET = 'GET'
    POST = 'POST'


# Constants to fill by each user
PS3838_USERNAME = ""
PS3838_PASSWORD = ""


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
    response = req.json()
    # f = open('sport_result2.json', 'w')
    # json_obj = json.dumps(response, indent=4)
    # f.write(json_obj)
    # f.close()
    return response

def get_balance():
    operation = '/v2/client/balance'
    req = requests.get(
        get_operation_endpoint(operation),
        headers=get_headers(HttpMethod.GET)
    )
    resp = req.json()
    bal = resp['availableBalance']
    return bal

def get_leagues(_id):
    operation = '/v3/leagues'
    req = requests.get(
        get_operation_endpoint(operation),
        headers=get_headers(HttpMethod.GET),
        params= {'sportId': _id}
    )
    response = req.json()
    return response


def get_period():
    operation = '/v1/periods'
    req = requests.get(
        get_operation_endpoint(operation),
        headers=get_headers(HttpMethod.GET),
        params= {'sportId': 29}
    )
    return req.json()

def get_line(bet_data):
    operation = '/v2/line'
    league_id = get_league_id(bet_data['league_name'])
    req_params = {'leagueId': league_id,
                  'handicap': bet_data['handicap'],
                  'oddsFormat': 'DECIMAL',
                  'sportId': bet_data['sport_id'],
                  'eventId': bet_data['event_id'],
                  'periodNumber': bet_data['period_number'],
                  'betType': bet_data['bet_type'],
                  'team': bet_data['team'],
                  'side': bet_data['side']
                  }
    req = requests.get(
        get_operation_endpoint(operation),
        headers=get_headers(HttpMethod.GET),
        params= req_params
    )
    data = req.json()
    try:
        line_id = data['lineId']
        altLineId = data['altLineId']
    except:
        print(f'>>>>> Invalid Alert. ')
        line_id = None
        altLineId = None
    return line_id, altLineId

def get_league_id(league_name):
    f = open('league_results.json', 'r')
    data = json.load(f)
    for d in data:
        leagues = d['leagues']
        for league in leagues:
            if league['name'] == league_name:
                return league['id']
                
    return None

       
    

def place_bet(bet_data):
    operation = '/v2/bets/place'
    
    payload = {'uniqueRequestId': str(uuid4()), 
                  
                  'oddsFormat': 'DECIMAL',
                  'acceptBetterLine': True,
                  'sportId': bet_data['sport_id'],
                  'lineId': bet_data['line_id'],
                  'altLineId': bet_data['altLineId'],
                  'eventId': bet_data['event_id'],
                  'periodNumber': bet_data['period_number'],
                  'betType': bet_data['bet_type'],
                  'team': bet_data['team'],
                  'side': bet_data['side'],
                  'stake': bet_data['kelly_stake'],
                  'winRiskStake': 'RISK',
                  'fillType': 'FILLANDKILL',
                  'pitcher1MustStart': True,
                  'pitcher2MustStart': True,
                  'handicap': bet_data['handicap']
                  
                  }
    req = requests.post(
        get_operation_endpoint(operation),
        headers=get_headers(HttpMethod.POST),
        json = payload
    )
    return req.json()



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
    elif id == '3':
        team = 'TEAM1'
    elif id == '4':
        team == 'TEAM2'
        
    
    return team

def parse_side(id):
    if id == '0':
        side = 'OVER'
    elif id == '1':
        side = 'UNDER'
    return side


def parse_bet_info(bet_info, max_risk_stake):
    bet_link = bet_info['direct_link']
    line = bet_info['market_and_bet_type_param']
    balance = get_balance()
    stake = getKelly(bet_info['koef'], balance, max_risk_stake)
    
    bet_data = {}
    bet_link = bet_link.replace('/', '|')
    data = bet_link.split('|')
    bet_data['event_id'] = bet_info['bookmaker_event_direct_link']
    bet_data['line_id'] = data[1]
    bet_data['sport_id'] = get_sport_id(bet_info['sport_id'])
    bet_data['league_name'] = bet_info['league']
    bet_type = parse_bet_type(data[3])
    bet_data['bet_type'] = bet_type
    bet_data['period_number'] = data[4]
    bet_data['kelly_stake'] = stake
    if bet_type == 'MONEYLINE':
        bet_data['handicap'] = None
        bet_data['side'] = None
        bet_data['team'] = parse_team(data[5])
    elif bet_type == 'TOTAL_POINTS':
        bet_data['handicap'] = line
        bet_data['side'] = parse_side(data[5])
        bet_data['team'] = None
    elif bet_type == 'TEAM_TOTAL_POINTS':
        bet_data['handicap'] = line
        bet_data['side'] = parse_side(data[5])
        bet_data['team'] = parse_team(data[6])
    elif bet_type == 'SPREAD':
        bet_data['handicap'] = line
        bet_data['side'] = None
        bet_data['team'] = parse_team(data[5])
    
    return bet_data

def get_all_leagues():
    f = open('sport_result.json', 'r')
    data = json.load(f)
    
    sports = data['sports']
    
    league_file = open('league_results.json', 'a')
    league_data = []
    for sport in sports:
        leagues = {}
        sp_id = sport['id']
        response = get_leagues(sp_id)
        results = response['leagues']
        leagues['sportId'] = sp_id 
        leagues['leagues'] = results
        league_data.append(leagues)
        sleep(0.5)
        
    json_obj = json.dumps(league_data, indent=4)
    league_file.write(json_obj)
    league_file.close()
    f.close()

def show_leagues():
    f = open('league_results.json', 'r')
    data = json.load(f)
    leagues = data['leagues']
    print(leagues)


def get_sport_id(bb_id):
    f = open('sport_result.json', 'r')
    data = json.load(f)
    sports = data['sports']
    for sport in sports:
        if sport['bb_id'] == bb_id:
            ps_id = sport['id']
            return ps_id
    return None
    
    
def getKelly(odds:float, bal:float, fraction:float) -> dict:
    
    p = 1/odds
    adjusted_stake = fraction * p * bal
    adjusted_stake = round(adjusted_stake)
    if adjusted_stake < 5:
        return 5
    
    return adjusted_stake
