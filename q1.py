# Python 3.8.6 (default, Oct 10 2020, 07:54:55)

#Print the top 5 symbols with quote asset BTC and the highest volume over the last 24 hours in descending order.

import requests
import json

def getVolume(elem):
    return float(elem['volume'])

url = 'https://api.binance.com/api/v3/ticker/24hr'
response = requests.get(url)

symbols = json.loads(response.text)

filteredsymbols = list(filter(lambda x: x['symbol'].endswith("BTC"), symbols))
filteredsymbols.sort(key=getVolume,reverse=True)

i = 1
print("TOP 5 symbols with quote asset BTC sorted by highest volume over last 24h in descending order\n")
for symbol in filteredsymbols:
    print("TOP ", i)
    print(symbol['symbol'])
    print('volume: ', symbol['volume'], '\n')
    i = i + 1
    if i == 6:
        break