import requests
from twilio.rest import Client

STOCK_NAME = "Tsla"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co//query"
NEWS_ENDPOINT = "https:/newsapi.org/v2/everything"

STOCK_API_KEY = "P9EFGEHSDFSDF"
NEWS_API_KEY = "2c5a322de98msd5f45f747gfff89dfdffd"
TWILIO_SIO = "AC6182316b77gh3553fk98989dfd99898"
TWILIO_AUTH_TOKEN = "45blo9898s5kjk54k4h898hhs999090dd90"


stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY
}

response = requests.get(STOCK_ENDPOINT,params=stock_params)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4, close"]
print(yesterday_closing_price)

day_before_yesterday_closing_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_closing_data["4, close"]

difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)

up_down = None
if difference > 0:
    up_down = "--/\--"
else:
    up_down = "--\/--"

difference_percentage = (difference / float(yesterday_closing_price)) * 100

if abs(difference_percentage) > 1:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,

    }

    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]

    three_articles = articles[:3]

   formatted_articles =  \
       [f"{STOCK_NAME}: {up_down}{difference_percentage}%\n" \
        f"Headline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]

   client = Client(TWILIO_SIO, TWILIO_AUTH_TOKEN)

   for article in formatted_articles:
    message = client.messages.create(
        body=article,
        from_= "+918899889988",
        to="+919988998899"
    )


