import pandas as pd
data = pd.read_csv('./methods/SOL-USD.csv')

def calcRSI(period):
    # Calculate price changes
  data['Price Change'] = data['Close'].diff()

  # Separate gains (positive changes) and losses (negative changes)
  data['Gain'] = data['Price Change'].apply(lambda x: x if x > 0 else 0)
  data['Loss'] = data['Price Change'].apply(lambda x: abs(x) if x < 0 else 0)

  # Calculate average gains and losses over the period
  data['Avg Gain'] = data['Gain'].rolling(window=period).mean()
  data['Avg Loss'] = data['Loss'].rolling(window=period).mean()

  # Calculate Relative Strength (RS)
  data['RS'] = data['Avg Gain'] / data['Avg Loss']

  # Calculate RSI
  data['RSI'] = 100 - (100 / (1 + data['RS']))
  print(data['RSI'].tail()) 
  return data['RSI']

  


def initDT():
  calcRSI(14)