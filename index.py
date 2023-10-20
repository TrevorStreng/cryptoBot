import os
from dotenv import load_dotenv
import ccxt
# import pandas as pd
import time

# TODO
# 1. get correct amount after trade and keep track of how much capital you have
# 2. log trades
# 3. determine if algorithm is performing better than the market
# 4. look into rsi

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

symbol = 'SOL/USDT'
timeframes = [5, 8, 13] # must be in order
# timeframes = ['7d', '25d', '99d']
averages = []
amount = -1 # This is the amount of money I am using in USD
money = 100.07
curPrice = -1
closes = []
bought = False

###### * sums closing prices of the past x days
def calcAvg():
  global closes
  global averages
  global timeframes
  total = 0
  i = 0
  cnt = 1
  averages = []
  for x in reversed(closes):
    total += x
    # print(timeframes, x)
    if cnt == timeframes[i]:
      # print(cnt)
      averages.append(total / timeframes[i])
      i += 1
    cnt += 1
  print(averages)
    




def start():
  global closes
  global timeframs
  days = exchange.fetchOHLCV(symbol, '1m')
  i = 0
  total = 0
  closes = [day[4] for day in days[-timeframes[(len(timeframes)-1)]:]]
  # print(closes)
  calcAvg()



def init():
  global averages
  global bought
  start()
  if not bought and averages[0] > averages[2] and averages[1] > averages[2]:
    if exchange.has['createMarketOrder']:
      # exchange.createMarketBuyOrder(symbol, amount, params = {})
      # exchange.fetchBalance(params = {})
      print('bought')
      bought = True
  elif bought and averages[0] < averages[2] and averages[1] < averages[2]:
      # !need to get amount avialable
    if exchange.has['createMarketOrder']:
      # order = exchange.createMarketSellOrder(symbol, params = {})
      # print(order)
      # amount = order.amount
      # print(amount)
      print('sold')
      bought = False
  else:
    print('didnt buy or sell')
  
  balance = exchange.fetchBalance(params = {})
  print(balance)

timer = 0
while(True):
  print('running at time:', timer)
  init()
  time.sleep(1 * 60)
  timer += 1
  if timer >= 60:
    break


# def testBuy():
#   if exchange.has['createMarketOrder']:
#     orderBuy = exchange.createMarketBuyOrder(symbol, amount, params = {})
#     print('buy order: ', orderBuy)


# def testSell():
#   if exchange.has['createMarketOrder']:
#     print(amount)
#     orderSell = exchange.createMarketSellOrder(symbol, amount, params = {'useBnb': True})
#     print('sell order: ', orderSell)

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