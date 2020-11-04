# Python 3.8.6 (default, Oct 10 2020, 07:54:55)

#Print the top 5 symbols with quote asset USDT and the highest number of trades over the last 24 hours in descending order.

import requests
import json

def getTrades(elem):
    return elem['count']

url = 'https://api.binance.com/api/v3/ticker/24hr'
response = requests.get(url)

symbols = json.loads(response.text)

filteredsymbols = list(filter(lambda x: x['symbol'].endswith("USDT"), symbols))
filteredsymbols.sort(key=getTrades,reverse=True)

i = 1
print("TOP 5 symbols with quote asset USDT sorted by highest trades over last 24h in descending order\n")
for symbol in filteredsymbols:
    print("TOP ", i)
    print(symbol['symbol'])
    print('with ', symbol['count'], ' trades\n')
    i = i + 1
    if i == 6:
        break