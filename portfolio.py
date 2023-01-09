import requests
import json
import argparse
from forex_python.converter import CurrencyRates

def get_coin_avg(coin: dict):
    slug = coin['slug']
    base_url = f"https://api.coinmarketcap.com/data-api/v3/cryptocurrency/market-pairs/latest?slug={slug}&start=1&limit=100&category=spot&centerType=all&sort=cmc_rank_advanced"
    r = requests.get(base_url, headers={'Cache-Control': 'no-cache'})   
    data = r.json()

    cnt = 0
    total = 0
    for mp in data['data']['marketPairs']:
        if mp['marketPair'] == f"{data['data']['symbol']}/USD":
            cnt += 1
            total += mp['price']

    avg = total / cnt
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
        total += holding_value
        print(f"{coin['name']} average price over {cnt} exchanges: {avg}, holding in USD: {holding_value:.2f}")
    
    zar_amount = cr.convert('USD', 'ZAR', total)
    print(f"Total in USD: {total:.2f}")
    print(f"Total in ZAR: {zar_amount:.2f}")


if __name__ == '__main__':
    main()