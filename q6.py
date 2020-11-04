# Python 3.8.6 (default, Oct 10 2020, 07:54:55)

# Make the output of Q5 accessible by querying http://localhost:8080/metrics using the Prometheus Metrics format.

import requests
import json
import time

import threading
from flask import Flask

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

app = Flask(__name__)

@app.before_first_request
def metrics_thread():
    def run():
        
        global datas
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
            time.sleep(10.0)

    thread = threading.Thread(target=run)
    thread.start()
 
def wrapString(string):
    return '<pre>' + string + '</pre>'

def generateMetric(metricName, metricDescription, symbol, value):
    result = ''
    result = result + '# HELP ' + metricName + ' ' + metricDescription +'\n'
    result = result + '# TYPE ' + metricName + ' gauge\n'
    result = result + metricName +'{symbol="' + symbol + '"} ' + value +'\n'
    return result

def exposeMetrics(datas):
    result = ''
    for key in datas:
        result = result + generateMetric('price_spread','price spread of symbol', key, str(datas[key]['spread'])) + '\n'
        result = result + generateMetric('price_spread_delta','absolute delta from previous (last 10 sec) price spread of symbol', key, str(datas[key]['delta'])) + '\n'
    return wrapString(result)

@app.route('/metrics')
def start():
    return exposeMetrics(datas)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True, threaded=True)