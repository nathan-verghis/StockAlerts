# Imports
import sys
import alerts
import json
from datetime import datetime

# stocks must be a dictionary of stock ticker names with values of at least `lower_bound` and/or `upper_bound`
def get_tickers(stocks_filename):
    # Get the users configurations
    with open(stocks_filename, 'r') as f:
        stocks = json.load(f)
    
    # Endlessly running background process (Until killed that is)
    while True:
        now = datetime.now()
        market_close = datetime(datetime.now().year, datetime.now().month, datetime.now().day, 17, 0, 0, 0)
        market_open = datetime(datetime.now().year, datetime.now().month, datetime.now().day, 19, 0, 0, 0)

        # Check if its trading time. Otherwise do nothing and waste a little resources
        if now > market_open and now < market_close:
            for stock_name in stocks.keys():
                if stock_name != "User":
                    # Time to track some STONKS
                    lower = stocks[stock_name]["lower_bound"]
                    upper = stocks[stock_name]["upper_bound"]
                    alerts.tracker(stock_name, upper, lower, stocks["User"])



if __name__ == "__main__":
    get_tickers(sys.argv[1])
