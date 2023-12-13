import math

# !need to use limit order for sell because market order price is constantly changing. I think

def initMovAvg(exchange, symbol, timeframes, logging, bought):
  symbols = createSymbols(symbol)
  averages = start(exchange, symbol, timeframes)
  if not bought and averages[0] > averages[2] and averages[1] > averages[2]:
    if exchange.has['createMarketOrder']:
      bal1 = float(getBalance(exchange, symbols[1])) # ^ need to get the amount of usdt to see how much SOL to buy
      orderbook = exchange.fetch_order_book(symbol)
      ask = float(orderbook['asks'][0][0] if len (orderbook['asks']) > 0 else None)
      amount = float(math.floor((bal1 / ask) * 100)/100)
      # amount = round(bal1 / ask, 2) if round(bal1 / ask, 2) > 0.01 else 0.01  # Ensure the minimum trade amount is met
      print('amount: ', amount)
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
      # amount = float(round(getBalance(exchange, symbols[0]),2)) # ^ need to get the amount of SOL to see how much to sell
      amount = float(math.floor(getBalance(exchange, symbols[0])*100)/100)
      print('amount: ', amount)

      # order = exchange.createMarketSellOrder(symbol, amount, params = {})
      orderbook = exchange.fetch_order_book(symbol)
      bid = float(orderbook['bids'][0][0] if len(orderbook['bids']) > 0 else None)
      order = exchange.createLimitSellOrder(symbol, amount, bid, params = {})
      print(order)
      bought = False
      logging.info('Sold: %s', order)
      print('sold')
      logging.info('amount: %s', amount)
  else:
    print('didnt buy or sell')
    # logging.info('Nothing happened')
  return bought

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
  # print(closes)
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
  # print(averages)
  return averages
  