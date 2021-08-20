from datetime import datetime
from time import sleep
import sys
import yfinance as yf
import pandas as pd
from yfinance import ticker
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

with open("sendgrid.env", "r") as f:
    SENDGRID_API_KEY = f.readline()

def check_ticker(ticker_name):
    data = yf.download(ticker_name, period='5m', interval='1m', progress=False)
    return data

def crossed_threshold(data, upper, lower):
    crossed_rows = []
    for index, row in data.iterrows():
        if lower is not None:
            if row["Adj Close"] < lower:
                crossed_rows.append((index, row))
        if upper is not None:
            if row["Adj Close"] > upper:
                crossed_rows.append((index, row))
    return crossed_rows

def tracker(ticker_name, upper, lower, user):
    market_close = datetime(datetime.now().year, datetime.now().month, datetime.now().day, 17, 0, 0, 0)
    now = datetime.now()
    while now != market_close:
        if now.minute % 5 == 0:
            df = check_ticker(ticker_name)
            crossed_rows = crossed_threshold(df, upper, lower)
            if len(crossed_rows) > 0:
                email_body = "<h3>Hello " + user["name"] + ",  your stock alerts are below</h3>"
                for row in crossed_rows:
                    email_body += "<p>Alert at " + str(row[0]) + "\n" + str(row[1]) + "</p></br>"
                email_body += "<p>This was generated at " + str(now) + " . Thank you for using Nathan's stock alerts!</p>"
                message = Mail(from_email='nverghis@uoguelph.ca', to_emails=user["email"], subject="Stock Alert! [Important]", html_content=email_body)
                try:
                    sg = SendGridAPIClient(SENDGRID_API_KEY)
                    sg.send(message)
                except Exception as e:
                    print(e)
        now = datetime.now()
        sleep(20)

if __name__ == "__main__":  
    tracker("UBER", 40, 41, {"email": "nbverghis@gmail.com","name": "Nathan Verghis"})
