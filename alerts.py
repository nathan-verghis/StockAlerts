from datetime import datetime
from time import sleep
import yfinance as yf
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

with open("sendgrid.env", "r") as f:
    # Yeah, you wish you knew what it was... (jk I'm on the free tier)
    SENDGRID_API_KEY = f.readline()

def check_ticker(ticker_name):
    # Get data using this beautiful api that's... you guessed it. FREE :)
    data = yf.download(ticker_name, period='5m', interval='1m', progress=False)
    return data

def crossed_threshold(data, upper, lower):
    crossed_rows = []

    # Check if user has set any boundaries, and if they've been crossed. Return bounds that have been
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

    # Continually check until its market close
    while now != market_close:
        if now.minute % 5 == 0:
            df = check_ticker(ticker_name)
            crossed_rows = crossed_threshold(df, upper, lower)

            # The bounds have been crossed! Time to buy crypto
            if len(crossed_rows) > 0:
                email_body = "<h3>Hello " + user["name"] + ",  your stock alerts are below</h3>"

                # Create basic email body of alerts
                for row in crossed_rows:
                    email_body += "<p>Alert at " + str(row[0]) + "\n" + str(row[1]) + "</p></br>"
                email_body += "<p>This was generated at " + str(now) + " . Thank you for using Nathan's stock alerts!</p>"
                message = Mail(from_email='nverghis@uoguelph.ca', to_emails=user["email"], subject="Stock Alert! [Important]", html_content=email_body)

                # Send that email! (In the future I'd like to look into using an SMS api cuz who checks their email?)
                try:
                    sg = SendGridAPIClient(SENDGRID_API_KEY)
                    sg.send(message)
                except Exception as e:
                    print(e)
        now = datetime.now()

        # Don't run nonsensically. As it is the check is only done every 5 mins.
        sleep(20)

# Ignore this. This is just for me to figure out my smooth-brain moments.
if __name__ == "__main__":  
    tracker("UBER", 40, 41, {"email": "nbverghis@gmail.com","name": "Nathan Verghis"})
