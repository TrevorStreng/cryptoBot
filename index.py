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

symbol = 'ETH/USDT'
timeframes = [5, 8, 13] # must be in order
# timeframes = ['7d', '25d', '99d']
averages = []
amount = -1 # This is the amount of money I am using in USD
money = 49.87
curPrice = -1
closes = []

###### * sums closing prices of the past x days
def calcAvg():
  global closes
  global averages
  global timeframes
  total = 0
  i = 0
  for x in closes:
    total += x[1] # & temp
    # total += x
    if x == timeframes[i]:
      averages.push(total / timeframes[i])
      # if i == len(timeframes)-1:
      #   break ####### ! this shouldn't be needed because closes should only be the length of the last timeframe
      i += 1
  print(averages)
    




def start():
  global closes
  global timeframs
  days = exchange.fetchOHLCV(symbol, '1d') # this returns a lot of days
  # print(days)
  i = 0
  total = 0
  closes = [[day[0], day[4]] for day in days[-timeframes[(len(timeframes)-1)]:]]
  print(closes)



def init():
  bought = False
  start()
  # if not bought and averages[0] > averages[2] and averages[1] > averages[2]:
  #   if exchange.has['createMarketOrder']:
  #     exchange.createMarketBuyOrder(symbol, amount, params = {})
  #     bought = True
  # if bought and averages[0] < averages[2] and averages[1] < averages[2]:
  #     # !need to get amount avialable
  #   if exchange.has['createMarketOrder']:
  #     order = exchange.createMarketSellOrder(symbol, params = {})
  #     print(order)
  #     amount = order.amount
  #     print(amount)
  #     bought = False


init()

def testBuy():
  if exchange.has['createMarketOrder']:
    orderBuy = exchange.createMarketBuyOrder(symbol, amount, params = {})
    print('buy order: ', orderBuy)


def testSell():
  if exchange.has['createMarketOrder']:
    print(amount)
    orderSell = exchange.createMarketSellOrder(symbol, amount, params = {'useBnb': True})
    print('sell order: ', orderSell)

def testCandles(timeframe):
  days = exchange.fetchOHLCV(symbol, timeframe)
  print(days)

# testCandles('1d')

def getPrice():
  global amount
  orderbook = exchange.fetchOrderBook(symbol)
  bid = orderbook['bids'][0][0] if len (orderbook['bids']) > 0 else None
  ask = orderbook['asks'][0][0] if len (orderbook['asks']) > 0 else None
  spread = (ask - bid) if (bid and ask) else None
  curPrice = bid
  print (exchange.id, 'market price', { 'bid': bid, 'ask': ask, 'spread': spread })
  print('calculating amount to buy now')
  # ^ Calculating the amount to buy
  amount = money / curPrice
  print(amount)
  # amount = round(amount, 2)
  # print(amount)
  # testSell()
  # testBuy()


# getPrice()