import os
from dotenv import load_dotenv
import ccxt
import pandas as pd

load_dotenv()

exchange = ccxt.binanceus({
  'apiKey': os.getenv('BINANCE_API_KEY'),
  'secret': os.getenv('BINANCE_API_SECRET'),
  'rateLimit': 2000,
  'enabledRateLimit': True,
  "urls": {
    'api': {
        'public': 'https://api.binance.us/api',
        'private': 'https://api.binance.us/api',
    }
  }
})

symbol = 'ETH/USD'
ticker = exchange.fetch_ticker(symbol)

# eth_price = ticker['last']

print(symbol)

# def fetch_data(ticker):
#   global exchange
#   bars,ticker_df = None, None

#   try: 
#     bars = exchange.fetch_ohlcv(ticker, timeframe='{CANDLE_DURATION_IN_MIN}m', limit=100)
#   except:
#     print(f"Error in fetching data from the exchange: {ticker}")

#   if bars is not None:
#     ticker_df = pd.DataFrame(bars[:-1], colums=['at', 'open', 'high', 'low', 'close', 'vol'])
#     ticker_df['Date'] = pd.to_datetime(ticker_df['at'], unit='ms')
#     ticker_df['symbol'] = ticker

#   return ticker_df

# fetch_data('ETH')