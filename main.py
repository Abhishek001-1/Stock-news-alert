import requests
from twilio.rest import Client

# from requests import get
stock_name = "TSLA"
company_name = "Tesla,Inc."

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

stock_api_key = "WHEBOB2K9FGFYIZF"
news_api_key = "71c5540684a64d71bdecc3f90bb930e0"
twilio_sid = "ENTER YOUR TWILIO SID"
twilio_auth_token = "ENTER YOUR TWILIO AUTH TOKEN"

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": stock_name,
    "apikey": stock_api_key,
}
response = requests.get(STOCK_ENDPOINT, params=stock_params)
# print(response.json())
data = response.json()["Time Series (Daily)"]
# print(data)
data_list = [value for (key, value) in data.items()]
# print(data_list)
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]
# print(yesterday_closing_price)

# todo Get the day before yesterday's closing stock price
day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]
# print(day_before_yesterday_closing_price)

# todo Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20. Hint: https://www.w3schools.com/python/ref_func_abs.asp
difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
# print(difference)
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"
# print(up_down)

# todo Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.
diff_percent = round((difference / float(yesterday_closing_price)) * 100)
# print(diff_percent)


# Step-2
## STEP 2: Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

# Instead of printing ("Get News"), use the News API to get articles related to the COMPANY_NAME.
# If difference percentage is greater than 5 then print("Get News").
if abs(diff_percent) > 1:
    news_params = {
        "apiKey": news_api_key,
        "qInTitle": company_name,
    }

    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    # print(news_response.json())
    articles = news_response.json()["articles"]
    # print(articles)

    # Use Python slice operator to create a list that contains the first 3 articles. Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation
    three_articles = articles[:3]
    # print(three_articles)

    # STEP 3: Use Twilio to send a seperate message with each article's title and description to your phone number.

    # Create a new list of the first 3 article's headline and description using list comprehension.
    formatted_articles = [
        f"{stock_name}: {up_down}{diff_percent}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for
        article in three_articles]
    # print(formatted_articles)
    # Send each article as a separate message via Twilio.
    client = Client(twilio_sid, twilio_auth_token)
#
#     #TODO - Send each article as a separate message via Twilio.
    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_="ENTER TWILIO NUMBER",
            to="ENTER DESTINATION NUMBER"
        )
        # print(message.status)
