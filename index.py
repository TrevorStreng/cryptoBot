import os
from dotenv import load_dotenv
import ccxt
import time
from methods.movingAvg import init 

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
amount = -1 # This is the amount of money I am using in USD
money = 100.07
curPrice = -1
bought = False

timer = 0
while(True):
  print('running at time:', timer)
  init(exchange, symbol, timeframes)
  time.sleep(1 * 60)
  timer += 1
  if timer >= 60:
    break


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
