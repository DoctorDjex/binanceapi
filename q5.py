# Python 3.8.6 (default, Oct 10 2020, 07:54:55)

#Every 10 seconds print the result of Q4 and the absolute delta from the previous value for each symbol.

import requests
import json
import time
from os import system, name 

def clearConsole():
    if name == 'nt': 
        _ = system('cls')
    else: 
        _ = system('clear') 

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
    

datas = {}
while True:
    
    symbols = takeSymbolsFromQ2()
    
    for symbol in symbols:
        newSpread = getPriceSpread(symbol)
        
        if symbol not in datas:
            datas[symbol] = {}
        if 'spread' not in datas[symbol]:
            datas[symbol]['spread'] = 0
        
        
        datas[symbol]['delta'] = abs(newSpread - datas[symbol]['spread'])
        datas[symbol]['spread'] = newSpread
        
        print('Symbol: ',symbol)
        print('Price new spread: ', datas[symbol]['spread'])
        print('Price spread delta: ', datas[symbol]['delta'])
    
    time.sleep(10.0)
    clearConsole()