from pprint import pprint
import json
import logging
import requests
import time
from datetime import datetime

def parse_bb_tips():
    for i in range(50):
        url = "https://rest-api-pr.betburger.com/api/v1/valuebets/bot_pro_search"
        headers = {
            'accept': "application/json",
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        

        response = requests.request("POST", url=url, headers=headers, params={
            'access_token': "token",
            'per_page': 50,
            'search_filter': [370233]
        })
        # print(response.url)
        # pprint(response, sort_dicts=False)
        
        response = response.json()
        print(response)
        bets = response['bets']
        valid_bets = []
        for b in bets:
            try:
                if b['is_value_bet']:
                    valid_bets.append(b)
            except:
                pass
        bb_events = []
        for bet in valid_bets:
            data = {}
            data['away'] = bet['away']
            data['home'] = bet['home']
            data['league'] = bet['league_name']
            data['price'] = bet['koef']
            # data['price'] = bet['koef']
            # data['bookmaker'] = bookmakers[bet['bookmaker_id']]
            data['bet_type'] = bet['market_and_bet_type']
            data['bet_type_value'] = bet['market_and_bet_type_param']
            data['sport_id'] = bet['sport_id']
            try:
                data['current_score'] = bet['current_score'].split(' ')[0]
            except:
                pass
            data['period_id'] = bet['period_id']
            data['start_time'] = datetime.fromtimestamp(bet['started_at']-3600).strftime('%Y-%m-%dT%H:%M:%SZ')
            bb_events.append(data)
