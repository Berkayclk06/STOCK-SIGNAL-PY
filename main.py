import requests
from twilio.rest import Client
from datetime import datetime, timedelta


STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
account_sid = # ACC SID
auth_token = # AUTH TOKEN
BEFORE_YESTERDAY = datetime.today() - timedelta(days=2)
YESTERDAY = datetime.today() - timedelta(days=1)
BEFORE_YESTERDAY = BEFORE_YESTERDAY.strftime("%Y-%m-%d")
YESTERDAY = YESTERDAY.strftime("%Y-%m-%d")

alpha_param = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": # API KEY,
}

r_alpha = requests.get("https://www.alphavantage.co/query", params=alpha_param)
r_alpha.raise_for_status()
alpha_data = r_alpha.json()

news_param = {
    "q": "Tesla",
    "from": BEFORE_YESTERDAY,
    "sortBy": "popularity",
    "apiKey": # API KEY,
}

r_news = requests.get("https://newsapi.org/v2/everything", params=news_param)
r_news.raise_for_status()
news_data = r_news.json()

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

stock_yst = alpha_data["Time Series (Daily)"][YESTERDAY]
stock_bf = alpha_data["Time Series (Daily)"][BEFORE_YESTERDAY]

close_diff = 100 * ((float(stock_yst["1. open"]) - float(stock_bf["4. close"])) / float(stock_bf["4. close"]))

close_diff = round(close_diff, 2)

if close_diff < 0:
    arrow = "🔻"
else:
    arrow = "🔺"

messages = (f"{STOCK}:{arrow}{close_diff}",
            f"Headline: {news_data['articles'][0]['title']} \nBrief: {news_data['articles'][0]['description']}",
            f"Headline: {news_data['articles'][1]['title']} \nBrief: {news_data['articles'][1]['description']}",
            f"Headline: {news_data['articles'][2]['title']} \nBrief: {news_data['articles'][2]['description']}")

for i in range(4):
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
        body=messages[i],
        from_= #TWILIO PHONE,
        to= #PERSONEL PHONE
    )

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.


## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 


# Optional: Format the SMS message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""
