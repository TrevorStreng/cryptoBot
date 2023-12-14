import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# & pink is used for steps


def initDT(exchange,symbols, bought):
  # ohlcv = exchange.fetch_ohlcv(symbol, timeframe) #! need to set timeframe
  df = pd.read_csv('./methods/SOL-USD.csv')
  df['Date'] = pd.to_datetime(df['Date'])
  # print(df.head())

  # & Preprocessing
  # filling all empty values with the average of the column
  numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
  df[numeric_columns] = df[numeric_columns].fillna(df[numeric_columns].mean())
  # ^ Possibly check for outliers and incosistancies

  # & Attempt 2 closing vs volume(learning)
  # m, b = np.polyfit()


  # & Attribute Selection
  df['Timestamp'] = pd.to_datetime(df['Date']).astype('int64')  # Convert to Unix timestamp
  # converting date to a number so I can obtain regression line
  x = df['Timestamp']
  y = df['Close']
  m, b = np.polyfit(x, df['Close'], 1)
  plt.figure(1)
  plt.scatter(x, y, label='Closing prices')
  plt.plot(x, m * x + b, color='red', label='Line of Best Fit')

  # Add labels and a legend
  plt.xlabel('X-axis')
  plt.ylabel('Y-axis')
  plt.title('Closing Price vs Day')
  plt.legend()

  # Display the plot
  plt.grid(True)

  # Predicted values using the linear regression model
  predicted_y = m * x + b

  residuals = y - predicted_y
  # Calculate absolute distances from the regression line
  # absolute_distances = np.abs(residuals)

  # print("Absolute distances:", absolute_distances)

  plt.figure(2)
  plt.title('Distance to regression line vs Volume')
  plt.scatter(df['Volume'], residuals)
  m1, b1 = np.polyfit(df['Volume'], residuals, 1)
  plt.plot(df['Volume'], m1 * df['Volume'] + b1, color='red', label='Line of Best Fit')

  plt.figure(3)
  plt.title('Close vs Volume')
  plt.scatter(df['Volume'], df['Close'])
  m2, b2 = np.polyfit(df['Volume'], df['Close'], 1)
  plt.plot(df['Volume'], m2 * df['Volume'] + b2, color='red')

  corr_coef = df['Close'].corr(df['Volume'])
  # print(corr_coef)

  # *Create model and test it
  # &Create model
  # Split the data into training and testing sets (e.g., 80% training and 20% testing)
  X_train, X_test, y_train, y_test = train_test_split(df[['Volume']], df[['Close']], test_size=0.2, random_state=42)

  model = LinearRegression()
  # Fit the model on the training data
  # & Train the model
  model.fit(X_train, y_train)
  # & Test the model
  # Test predicitions
  predictions = model.predict(X_test) # use the model to predict the test values 
  print(predictions)

  # val = 65000000
  # predict = model.predict(np.array(val).reshape(1, -1))
  # print('Value predicted: ', predict)
  # Calculate Mean Squared Error (MSE)
  mse = mean_squared_error(y_test, predictions)
  print(f"Mean Squared Error (MSE): {mse}")

  # Calculate Root Mean Squared Error (RMSE)
  rmse = mean_squared_error(y_test, predictions, squared=False)
  print(f"Root Mean Squared Error (RMSE): {rmse}")

  # Calculate Mean Absolute Error (MAE)
  mae = mean_absolute_error(y_test, predictions)
  print(f"Mean Absolute Error (MAE): {mae}")

  # Calculate R-squared (R²)
  r_squared = r2_score(y_test, predictions)
  print(f"R-squared (R²): {r_squared}")