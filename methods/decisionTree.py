import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

# & pink is used for steps


def initDT(exchange,symbols):
  # ohlcv = exchange.fetch_ohlcv(symbol, timeframe) #! need to set timeframe
  df = pd.read_csv('./methods/SOL-USD.csv')
  # print(df.head())
  df['timestamp'] = pd.to_datetime(df['timestamp'], units='ms')

  # & Preprocessing
  