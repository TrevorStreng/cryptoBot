import os
from dotenv import load_dotenv
import ccxt
# import pandas as pd
import time

load_dotenv()

exchange = ccxt.binanceus({
  'apiKey': os.getenv('BINANCE_API_KEY'),
  'secret': os.getenv('BINANCE_API_SECRET'),
  'rateLimit': 2000,
  'enabledRateLimit': True,
  "urls": {
    'api': {
        'public': 'https://api.binance.us/api/v3',
        'private': 'https://api.binance.us/api/v3',
    }
  }
})

symbol = 'ETH/USD'
timeframes = ['5d', '8d', '13d']
# timeframes = ['7d', '25d', '99d']
averages = []
# amount = 0.001 # This is the amount of money I am using in USD

###### * sums closing prices of the past x days
def calcMovingAvg(days):
  total = 0
  for i in days:
    total += i[4]
  total /= len(days)
  return total


def start(timeframe):
  days = exchange.fetchOHLCV(symbol, timeframe)
  print(days)
  # ! calcMovingAvg(days)
  averages.push(days)


def init():
  bought = False
  for x in timeframes:
    start(x)
  if not bought and averages[0] > averages[2] and averages[1] > averages[2]:
    if exchange.has['createMarketOrder']:
      exchange.createMarketBuyOrder(symbol, amount, params = {})
      bought = True
  if bought and averages[0] < averages[2] and averages[1] < averages[2]:
      # !need to get amount avialable
    if exchange.has['createMarketOrder']:
      order = exchange.createMarketSellOrder(symbol, params = {})
      print(order)
      amount = order.amount
      print(amount)
      bought = False


# init()

def testBuy():
  if exchange.has['createMarketOrder']:
    orderBuy = exchange.createMarketBuyOrder(symbol, 0.01, params = {})
    print('buy order: \n' + orderBuy)


def testSell():
  if exchange.has['createMarketOrder']:
    orderSell = exchange.createMarketSellOrder(symbol, 0.01, params = {})
    print('sell order: \n' + orderSell)

testBuy()

time.sleep(10)

testSell()