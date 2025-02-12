import requests
import json
import argparse
from forex_python.converter import CurrencyRates, RatesNotAvailableError
from googlesearch import search
from requests.exceptions import SSLError

def get_coin_avg(coin: dict):
    slug = coin['slug']
    base_url = f"https://api.coinmarketcap.com/data-api/v3/cryptocurrency/market-pairs/latest?slug={slug}&start=1&limit=100&category=spot&centerType=all&sort=cmc_rank_advanced"
    #  print(f"{base_url}")
    try:
        r = requests.get(base_url, headers={'Cache-Control': 'no-cache'})   
        data = r.json()
    except TimeoutError as e:
        print(f"Timeout getting {slug} data: {e}")

    cnt = 0
    total = 0
    for mp in data['data']['marketPairs']:
        if mp['marketPair'] == f"{data['data']['symbol']}/USD":
            cnt += 1
            total += mp['price']

    try:
        avg = total / cnt
    except ZeroDivisionError:
        return 0, 0, 0

    holding_value = avg * float(coin['holding'])
    return avg, cnt, holding_value

def main():

    cr = CurrencyRates()
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config_file", required=True,
                        help="Config file containing the trading pairs.")
    args = parser.parse_args()

    data = json.load(open(args.config_file))
    total = 0
    for coin in data['coins']:
        avg, cnt, holding_value = get_coin_avg(coin)
        if cnt != 0:
            total += holding_value
            print(f"{coin['name']} average price over {cnt} exchanges: {avg}, holding in USD: {holding_value:.2f}")
    
    print(f"Total in USD: {total:.2f}")
    try:
        zar_amount = cr.convert('USD', 'ZAR', total)
        print(f"Total in ZAR: {zar_amount:.2f}")
    except (RatesNotAvailableError, SSLError):
        print("python-forex converter not available. Googling... ")
        for r in search(f"{total} USD in ZAR", num_results=1, advanced=True):
            print("huh")
            print(r)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()
