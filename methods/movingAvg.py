import ccxt
import time


###### * sums closing prices of the past x days
def calcAvg(timeframes):
  global closes
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
  closes = [day[4] for day in days[-timeframes[(len(timeframes)-1)]:]]
  # print(closes)
  return calcAvg(timeframes)

def init(exchange, symbol, timeframes):
  #! global averages
  global bought
  symbols = createSymbols(symbol)
  averages = start(exchange, symbol, timeframes)
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
  
  balance = exchange.fetchBalance(params = {}).get(symbols[0])
  # print(balance.get('USDT'))

def createSymbols(symbol):
  return symbol.split('/') # 'SOL/USDT'