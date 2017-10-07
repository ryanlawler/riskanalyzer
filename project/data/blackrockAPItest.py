
import requests
import json
import numpy as np
import Queue

def dump(js):
    print json.dumps(js, indent=2)

def setParams(tickers):
    positions = ''
    distNum = 100 / len(tickers)
    for i in range(0, len(tickers)):
        positions = positions + tickers[i] + '~' + str(distNum)
        if i != len(tickers) - 1:
            positions += '|'
    return positions

def main(tickers):
    portfolioAnalysisRequest = requests.get("https://www.blackrock.com/tools/hackathon/portfolio-analysis", params={'positions' : setParams(tickers), 'calculateRisk': 'true'})
    performanceDataRequest = requests.get("https://www.blackrock.com/tools/hackathon/performance", params= {'identifiers':"IXN"})
    portfolioJson = portfolioAnalysisRequest.json()
    performanceJson = performanceDataRequest.json()
    holdings = portfolioJson['resultMap']['PORTFOLIOS'][0]['portfolios'][0]['holdings']
    tickers = []
    myList = []
    q = Queue.PriorityQueue()
    for holding in holdings:
        ticker = str(holding['ticker'])
        tickers.append(ticker)
        score = holding['riskData']['totalRisk']
        q.put(ticker, score)
        myList.append(score)
    mean_duration = np.mean(myList)
    std_dev_one_test = np.std(myList)
    def drop_outliers(x):
        if abs(x - mean_duration) <= 2 * std_dev_one_test:
            return x
    myList = filter(drop_outliers, myList)
    print('Your risk score: ', np.mean(myList))
    print('Your three most volatile stocks: ')
    for _ in range(0, 3):
        if not q.empty():
            print(q.get())

if __name__ == "__main__":
    params = ['MU', 'NVDA', 'SQM','AAPL', 'GOOG', 'DATA']
    main(params)