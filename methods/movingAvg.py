bought = False
def calcAvg(closes, timeframes):
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
  return averages

def start(exchange, symbol, timeframes):
  global closes
  global timeframs
  days = exchange.fetchOHLCV(symbol, '1m')
  i = 0
  total = 0
  closes = [day[4] for day in days]
  # closes = [day[4] for day in days[-timeframes[(len(timeframes)-1)]:]]
  # print(closes)
  return calcAvg(closes, timeframes)

def initMovAvg(exchange, symbol, timeframes):
  global bought
  symbols = createSymbols(symbol)
  averages = start(exchange, symbol, timeframes)
  if not bought and averages[0] > averages[2] and averages[1] > averages[2]:
    if exchange.has['createMarketOrder']:
      bal0 = getBalance(exchange, symbols[1]) # ^ need to get the amount of usdt to see how much SOL to buy
      print(bal0) # !!!! this prints none
      # order = exchange.createMarketBuyOrder(symbol, bal0, params = {})
      # print(order)
      print('bought')
      bought = True
  elif bought and averages[0] < averages[2] and averages[1] < averages[2]:
    if exchange.has['createMarketOrder']:
      bal1 = getBalance(exchange, symbols[0]).get(symbols[1]) # ^ need to get the amount of SOL to see how much to sell
      order = exchange.createMarketSellOrder(symbol, bal1, params = {})
      print(order)
      print('sold')
      bought = False
  else:
    print('didnt buy or sell')
  
  # balance = exchange.fetchBalance(params = {}).get(symbols[0])
  # print(balance.get('USDT'))

def createSymbols(symbol):
  return symbol.split('/') # 'SOL/USDT' returns array

def getBalance(exchange, symbol):
  exchange.fetchBalance(params={}).get(symbol)