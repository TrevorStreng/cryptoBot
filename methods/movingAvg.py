bought = False

# 1.
def initMovAvg(exchange, symbol, timeframes, logging):
  global bought
  symbols = createSymbols(symbol)
  averages = start(exchange, symbol, timeframes)
  if not bought and averages[0] > averages[2] and averages[1] > averages[2]:
    if exchange.has['createMarketOrder']:
      bal0 = getBalance(exchange, symbols[1]) # ^ need to get the amount of usdt to see how much SOL to buy
      orderbook = exchange.fetch_order_book (symbol)
      print(orderbook)
      ask = orderbook['asks'][0][0] if len (orderbook['asks']) > 0 else None
      print(ask)
      amount = bal0.get('free') / ask # amount that I want to buy
      print('amount: ', amount)
      order = exchange.createLimitBuyOrder(symbol, amount, ask, params = {})
      print(order)
      bought = True
      print('bought: ', bought)
      logging.info('Bought: ', order)
  elif bought and averages[0] < averages[2] and averages[1] < averages[2]:
    if exchange.has['createMarketOrder']:
      bal1 = getBalance(exchange, symbols[0]).get(symbols[1]) # ^ need to get the amount of SOL to see how much to sell
      # ! need to fix the selling
      # order = exchange.createMarketSellOrder(symbol, bal1.get('free'), params = {})
      # print(order)
      print('bought: ', bought)
      bought = False
  else:
    print('didnt buy or sell')
    logging.info('Nothing happened')

# 2.
def createSymbols(symbol):
  return symbol.split('/') # 'SOL/USDT' returns array

# 3.
def getBalance(exchange, symbol):
  return exchange.fetchBalance(params={}).get(symbol)

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
  