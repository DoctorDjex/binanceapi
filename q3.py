# Python 3.8.6 (default, Oct 10 2020, 07:54:55)

#Using the symbols from Q1, what is the total notional value of the top 200 bids and asks currently on each order book?

import requests
import json

def getVolume(elem):
    return float(elem['volume'])

def getSymbol(elem):
    return elem['symbol']

def takeSymbolsFromQ1():
    url = 'https://api.binance.com/api/v3/ticker/24hr'
    response = requests.get(url)
    symbols = json.loads(response.text)
    filteredsymbols = list(filter(lambda x: x['symbol'].endswith("BTC"), symbols))
    filteredsymbols.sort(key=getVolume,reverse=True)
    symbols = list(map(getSymbol, filteredsymbols)) 
    return symbols[:5]
    
def getBidOrAskPrice(elem):
    return float(elem[0])
    
def getNotionalValue(elem):
    return float(elem[0]) * float(elem[1])
   
def getTotalNotionalValueFor(symbol):
    #We want to get top 200 bids and top 200 asks for this order book
    #By definition, top bids represents highest bids, top asks represents lowest asks
    
    #so the idea is to firstly get the full order book (max 5000 bids and asks)
    limit = '5000'
    url = 'https://api.binance.com/api/v3/depth?symbol=' + symbol + '&limit='+limit
    response = requests.get(url)
    elements = json.loads(response.text)
    
    #then, from this order book, setting two arrays:
    # - one with all bids sorted by price in descending order
    # - one with all asks sorted by price in ascending order
    
    #for each of those we keep only 200 first values (top bids (highest price) and top asks (lowest price))
    bids = elements['bids']
    bids.sort(key=getBidOrAskPrice,reverse=True)
    bids = bids[:200]
    
    asks = elements['asks']
    asks.sort(key=getBidOrAskPrice,reverse=False)
    asks = asks[:200]
    
    #then we get notional value (price * qty)
    bidsNV = sum(list(map(getNotionalValue,bids)))
    asksNV = sum(list(map(getNotionalValue,asks)))
    
    #the question asked for "the total notional value" for bid and asks
    #so let's just sum up those two values
    total = bidsNV + asksNV
    
    print(symbol,'\n')
    print('Total notional value: ', total,'\n')
    

#First getting the symbols from Q1 with the same algorithm 
symbols = takeSymbolsFromQ1()
#then get the total for each one
for symbol in symbols:
    getTotalNotionalValueFor(symbol)