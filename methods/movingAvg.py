# 1.
def initMovAvg(exchange, symbol, timeframes, logging, bought):
  symbols = createSymbols(symbol)
  averages = start(exchange, symbol, timeframes)
  if not bought and averages[0] > averages[2] and averages[1] > averages[2]:
    if exchange.has['createMarketOrder']:
      bal1 = getBalance(exchange, symbols[1]) # ^ need to get the amount of usdt to see how much SOL to buy
      orderbook = exchange.fetch_order_book (symbol)
      print(orderbook)
      ask = orderbook['asks'][0][0] if len (orderbook['asks']) > 0 else None
      print(ask)
      amount = bal1 / ask # amount that I want to buy
      print('amount: %s', amount)
      order = exchange.createLimitBuyOrder(symbol, amount, ask, params = {})
      print(order)
      bought = True
      logging.info('Bought: ', order) # & Make sure to log price and amount bought
  elif bought and averages[0] < averages[2] and averages[1] < averages[2]:
    if exchange.has['createMarketOrder']:
      amount = getBalance(exchange, symbols[0]) # ^ need to get the amount of SOL to see how much to sell
      # orderbook = exchange.fetch_order_book (symbol)
      # print(orderbook)
      # bid = orderbook['bids'][0][0] if len (orderbook['bids']) > 0 else None
      # print(bid)
      order = exchange.createMarketSellOrder(symbol, amount, params = {})
      print(order)
      bought = False
      logging.info('Sold: %s', order)
  else:
    print('didnt buy or sell')
    logging.info('Nothing happened')

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
  