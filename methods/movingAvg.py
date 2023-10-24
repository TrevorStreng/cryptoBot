bought = False

# 1.
def initMovAvg(exchange, symbol, timeframes):
  global bought
  symbols = createSymbols(symbol)
  averages = start(exchange, symbol, timeframes)
  # bal = getBalance(exchange, symbols[1])
  # print(bal.get('free'))
  if not bought and averages[0] > averages[2] and averages[1] > averages[2]:
    if exchange.has['createMarketOrder']:
      bal0 = getBalance(exchange, symbols[1]) # ^ need to get the amount of usdt to see how much SOL to buy
      # ! need to calculate the amount of SOL to buy, might be tough with market orders

      # order = exchange.createMarketBuyOrder(symbol, bal0.get('free'), params = {})
      print(order)
      print('bought')
      bought = True
  elif bought and averages[0] < averages[2] and averages[1] < averages[2]:
    if exchange.has['createMarketOrder']:
      bal1 = getBalance(exchange, symbols[0]).get(symbols[1]) # ^ need to get the amount of SOL to see how much to sell
      # order = exchange.createMarketSellOrder(symbol, bal1.get('free'), params = {})
      print(order)
      print('sold')
      bought = False
  else:
    print('didnt buy or sell')

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
  