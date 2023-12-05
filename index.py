import os
from dotenv import load_dotenv
import ccxt
import time
from methods.movingAvg import initMovAvg 
from methods.movingAvg import getBalance 
from methods.movingAvg import createSymbols 
import logging
from datetime import date

# TODO
# 1. get correct amount after trade and keep track of how much capital you have
# 2. log trades and errors
# 3. determine if algorithm is performing better than the market
# 4. check where funds are to determine if bought or not
# 5. look into rsi

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
bought = False

timer = 0
log_file = 'crypto.log'
log_level = logging.INFO
logging.basicConfig(filename=log_file, level=log_level, format="%(asctime)s [%(levelname)s]: %(message)s")
def startTrading():
  # Log day
  global timer
  dates = date.today()
  logging.info('Date: %s/%s/%s', dates.month, dates.day, dates.year)
  symbols = createSymbols(symbol)
  bought = checkBought(symbols[1])
  print(bought)
  while(True):
    # print('running at time:', timer)
    bought = initMovAvg(exchange, symbol, timeframes, logging, bought)
    time.sleep(1 * 60)
    timer += 1
    if timer >= 60 * 5:
      break
logging.shutdown()

def checkBought(symb):
  return getBalance(exchange, symb) < 5

startTrading()