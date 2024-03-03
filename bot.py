from pprint import pprint
import json
import logging
import requests
import time
from datetime import datetime



def parse_bb_tips():
    f = open('results.json', 'a')
    valid_bets = []
    while True:
        time.sleep(10)
        url = "https://rest-api-pr.betburger.com/api/v1/valuebets/bot_pro_search"
        headers = {
            'accept': "application/json",
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        

        response = requests.request("POST", url=url, headers=headers, params={
            'access_token': "36971d55b71eea2308d5827cbe1e75e1", #bcdb92ef761f026b0f2b4737dddcabfe
            'per_page': 50,
            'search_filter': [396072] #765428 #396072
        })
        
        response = response.json()
        
        # pprint(response)
        bets = response['bets']
        
        for b in bets:
            try:
                if b['is_value_bet'] is True and b['id'] not in valid_bets:
                    valid_bets.append(b['id'])
                    json_obj = json.dumps(b, indent=4)
                    f.write(json_obj)
            except:
                pass
        bb_events = []
        # for bet in valid_bets:
        #     data = {}
        #     data['away'] = bet['away']
        #     data['home'] = bet['home']
        #     data['league'] = bet['league_name']
        #     data['price'] = bet['koef']
        #     data['bet_type'] = bet['market_and_bet_type']
        #     data['bet_type_value'] = bet['market_and_bet_type_param']
        #     data['sport_id'] = bet['sport_id']
        #     try:
        #         data['current_score'] = bet['current_score'].split(' ')[0]
        #     except:
        #         pass
        #     data['period_id'] = bet['period_id']
        #     data['start_time'] = datetime.fromtimestamp(bet['started_at']-3600).strftime('%Y-%m-%dT%H:%M:%SZ')
        #     bb_events.append(data)
    f.close()

parse_bb_tips()
