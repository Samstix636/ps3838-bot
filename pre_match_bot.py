from pprint import pprint
import json
import logging
import requests
import time
from datetime import datetime
from utils import parse_bet_info, place_bet, get_line


def parse_bb_tips():
    valid_bets = []
    while True:
        time.sleep(1)
        url = "https://rest-api-pr.betburger.com/api/v1/valuebets/bot_pro_search"
        headers = {
            'accept': "application/json",
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        response = requests.request("POST", url=url, headers=headers, params={
            'access_token': access_token, 
            'per_page': 50,
            'search_filter': [396072] 
        })
        
        response = response.json()
        
        bets = response['bets']
        
        for b in bets:
            try:
                if b['is_value_bet'] is True and b['id'] not in valid_bets:
                    print('===================================================================================')
                    print(f'>>>>> Alert for {b["home"]} vs {b["away"]} [{b["league_name"]}]')
                    valid_bets.append(b['id'])
                    bet_info = parse_bet_info(b, risk_fraction)
                    line_id, altLineId = get_line(bet_info)
                    if line_id is None:
                        continue
                    bet_info['line_id'], bet_info['altLineId'] = line_id, altLineId
                    print('>>>>> Bet INFO:\n', bet_info)
                    
                    bet_result = place_bet(bet_info)
                    try:
                        status = bet_result['status']
                        if status == 'PROCESSED_WITH_ERROR':
                            print(f'>>>>> Pre-match Bet not placed. {bet_result}')
                        print(f'>>>>> Pre-match Bet Status: {status}')
                    except:
                        print(f'>>>>> Pre-match Bet not placed. {bet_result["errorCode"]}')
            except:
                logging.error('Error', exc_info=True)
                continue
        



if __name__ == '__main__':
    test_amounts = [500, 1000, 10000]
    access_token = input('Copy and paste Betburger api token here >>>')
    while True:
        max_risk_percent = input('Enter Maximum percentage of balance to risk. (e.g 10) >>>')
        try:
            if float(max_risk_percent) > 100:
                raise ValueError('Maximum risk percentage must be less than 100')
            risk_fraction = float(max_risk_percent) / 100
        except Exception as e:
            logging.error('ERROR: Invalid input value entered', exc_info=True)
            
            continue
        
        print('-------------------------------------------------')
        for amount in test_amounts:
            test_stake = risk_fraction * amount
            print(f'For a bank roll of {amount}, the maximum possible stake amount is {test_stake}')
        
        print('-------------------------------------------------')
        to_continue = input('Do you want to launch bot? (y/n):')
        if to_continue == 'n':
            pass
        else:
            break
    print('>>>>> Bot is now running...')
    parse_bb_tips()
