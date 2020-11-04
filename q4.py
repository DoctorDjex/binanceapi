# Python 3.8.6 (default, Oct 10 2020, 07:54:55)

# What is the price spread for each of the symbols from Q2?

import requests
import json

def getTrades(elem):
    return elem['count']
    
def getSymbol(elem):
    return elem['symbol']
    
def takeSymbolsFromQ2():
    url = 'https://api.binance.com/api/v3/ticker/24hr'
    response = requests.get(url)
    symbols = json.loads(response.text)
    filteredsymbols = list(filter(lambda x: x['symbol'].endswith("USDT"), symbols))
    filteredsymbols.sort(key=getTrades,reverse=True)
    symbols = list(map(getSymbol, filteredsymbols)) 
    return symbols[:5]

def getPriceSpread(symbol):
    url = 'https://api.binance.com/api/v3/ticker/24hr?symbol=' + symbol
    response = requests.get(url)
    elements = json.loads(response.text)
    return float(elements['askPrice']) - float(elements['bidPrice'])
    
#First getting the symbols from Q2 with the same algorithm 
symbols = takeSymbolsFromQ2()

for symbol in symbols:
    print('Symbol: ',symbol)
    print('Price spread: ', getPriceSpread(symbol))