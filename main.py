import requests
from twilio.rest import Client
from datetime import datetime, timedelta
import os


STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
account_sid = os.environ["ACCOUNT_SID"]
auth_token = os.environ["AUTH_TOKEN"]

# GIVES SPECIFIED DAY ON STRING FORMAT.
BEFORE_YESTERDAY = datetime.today() - timedelta(days=2)
YESTERDAY = datetime.today() - timedelta(days=1)
BEFORE_YESTERDAY = BEFORE_YESTERDAY.strftime("%Y-%m-%d")
YESTERDAY = YESTERDAY.strftime("%Y-%m-%d")

# API REQS AND PARAMETERS.

alpha_param = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": os.environ["ALPHA_API_KEY"],
}

r_alpha = requests.get("https://www.alphavantage.co/query", params=alpha_param)
r_alpha.raise_for_status()
alpha_data = r_alpha.json()

news_param = {
    "q": "Tesla",
    "from": BEFORE_YESTERDAY,
    "sortBy": "popularity",
    "apiKey": os.environ["NEWS_API_KEY"],
}

r_news = requests.get("https://newsapi.org/v2/everything", params=news_param)
r_news.raise_for_status()
news_data = r_news.json()

# STOCK INFO OF SPECIFIED DAYS.
stock_yst = alpha_data["Time Series (Daily)"][YESTERDAY]
stock_bf = alpha_data["Time Series (Daily)"][BEFORE_YESTERDAY]

# CLOSING DIFFERENCES OF STOCKS.

close_diff = 100 * ((float(stock_yst["4. close"]) - float(stock_bf["4. close"])) / float(stock_bf["4. close"]))

close_diff = round(close_diff, 2)

# MESSAGE FORMAT.

if close_diff < 0:
    arrow = "🔻"
else:
    arrow = "🔺"

messages = (f"{STOCK}:{arrow}{close_diff}",
            f"Headline: {news_data['articles'][0]['title']} \nBrief: {news_data['articles'][0]['description']}",
            f"Headline: {news_data['articles'][1]['title']} \nBrief: {news_data['articles'][1]['description']}",
            f"Headline: {news_data['articles'][2]['title']} \nBrief: {news_data['articles'][2]['description']}")

for i in messages:
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
            body=i,
            from_=os.environ["FROM_PHONE"],
            to=os.environ["TO_PHONE"],
        )

