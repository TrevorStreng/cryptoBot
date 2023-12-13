import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import numpy as np

# & pink is used for steps


def initDT(exchange,symbols, bought):
  # ohlcv = exchange.fetch_ohlcv(symbol, timeframe) #! need to set timeframe
  df = pd.read_csv('./methods/SOL-USD.csv')
  df['Date'] = pd.to_datetime(df['Date'])
  # print(df.head())

  # & Preprocessing
  print(df.isnull().sum())
  numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
  df[numeric_columns] = df[numeric_columns].fillna(df[numeric_columns].mean())

  # df.fillna(df.mean(), inplace=True) # fill null values with the mean value

  print('2: \n',df.isnull().sum())

  # & Attribute Selection
