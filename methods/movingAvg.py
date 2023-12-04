# 1.
# ! Still gettng precision error
# amount: %s 0.0057042493744787325
# Traceback (most recent call last):
#   File "index.py", line 62, in <module>
#     startTrading()
#   File "index.py", line 52, in startTrading
#     initMovAvg(exchange, symbol, timeframes, logging, bought)
#   File "/home/pi/Documents/crypto_bot/cryptoBot/methods/movingAvg.py", line 14, in initMovAvg
#     order = exchange.createLimitBuyOrder(symbol, amount, ask, params = {})
#   File "/home/pi/.local/lib/python3.7/site-packages/ccxt/base/exchange.py", line 3640, in create_limit_buy_order
#     return self.create_order(symbol, 'limit', 'buy', amount, price, params)
#   File "/home/pi/.local/lib/python3.7/site-packages/ccxt/binance.py", line 4174, in create_order
#     request = self.create_order_request(symbol, type, side, amount, price, params)
#   File "/home/pi/.local/lib/python3.7/site-packages/ccxt/binance.py", line 4352, in create_order_request
#     request['quantity'] = self.amount_to_precision(symbol, amount)
#   File "/home/pi/.local/lib/python3.7/site-packages/ccxt/base/exchange.py", line 3666, in amount_to_precision
#     raise InvalidOrder(self.id + ' amount of ' + market['symbol'] + ' must be greater than minimum amount precision of ' + self.number_to_string(market['precision']['amount']))
# ccxt.base.errors.InvalidOrder: binanceus amount of SOL/USDT must be greater than minimum amount precision of 2

# *Im thinking that the amount im requesting to trade is more than available balance
# ^buy order seems to work sometimes

def initMovAvg(exchange, symbol, timeframes, logging, bought):
  symbols = createSymbols(symbol)
  averages = start(exchange, symbol, timeframes)
  if not bought and averages[0] > averages[2] and averages[1] > averages[2]:
    if exchange.has['createMarketOrder']:
      bal1 = float(getBalance(exchange, symbols[1])) # ^ need to get the amount of usdt to see how much SOL to buy
      orderbook = exchange.fetch_order_book (symbol)
      # print(orderbook)
      ask = float(orderbook['asks'][0][0] if len (orderbook['asks']) > 0 else None)
      # print(ask)
      # amount = bal1 / ask # amount that I want to buy
      amount = round(bal1 / ask, 2)
      print('amount: %s', amount)
      order = exchange.createLimitBuyOrder(symbol, amount, ask, params = {})
      # print(order)
      bought = True
      logging.info('Bought: %s', order) # & Make sure to log price and amount bought
      logging.info('amount bought: %s', amount)
      logging.info('balance before: %s', bal1)
      logging.info('ask: %s', ask)
      logging.info('order: %s', order)
  elif bought and averages[0] < averages[2] and averages[1] < averages[2]:
    if exchange.has['createMarketOrder']:
      amount = float(round(getBalance(exchange, symbols[0]),2)) # ^ need to get the amount of SOL to see how much to sell
      # orderbook = exchange.fetch_order_book (symbol)
      # print(orderbook)
      # bid = orderbook['bids'][0][0] if len (orderbook['bids']) > 0 else None
      # print(bid)
      order = exchange.createMarketSellOrder(symbol, amount, params = {})
      print(order)
      bought = False
      logging.info('Sold: %s', order)
      logging.info('amount: %s', amount)
  else:
    print('didnt buy or sell')
    # logging.info('Nothing happened')

# 2.
def createSymbols(symbol):
  return symbol.split('/') # 'SOL/USDT' returns array

# 3.
def getBalance(exchange, symbol):
  bal = exchange.fetchBalance(params={}).get(symbol)
  amount = bal.get('free')
  return amount

# 4.
def start(exchange, symbol, timeframes):
  global timeframs
  days = exchange.fetchOHLCV(symbol, '1m')
  i = 0
  total = 0
  closes = [day[4] for day in days[-timeframes[(len(timeframes)-1)]:]]
  print(closes)
  return calcAvg(closes, timeframes)

# 5.
def calcAvg(closes, timeframes):
  total = 0
  i = 0
  cnt = 1
  averages = []
  for x in reversed(closes):
    total += x
    if cnt == timeframes[i]:
      averages.append(total / timeframes[i])
      i += 1
    cnt += 1
  print(averages)
  return averages
  