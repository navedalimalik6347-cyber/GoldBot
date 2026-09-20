import os
import time
import google.generativeai as genai
import tweepy
import yfinance as yf

# API Keys setup (Yeh GitHub ke secrets se keys uthayega)
X_API_KEY = os.environ.get("X_API_KEY")
X_API_SECRET = os.environ.get("X_API_SECRET")
X_ACCESS_TOKEN = os.environ.get("X_ACCESS_TOKEN")
X_ACCESS_SECRET = os.environ.get("X_ACCESS_SECRET")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# Gemini configure karein
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")


def get_market_data():
  try:
    # Gold aur Bitcoin ka data fetch karna
    gold = yf.Ticker("GC=Z")
    btc = yf.Ticker("BTC-USD")

    gold_data = gold.history(period="1d")
    btc_data = btc.history(period="1d")

    gold_price = (
        gold_data["Close"].iloc[-1] if not gold_data.empty else "N/A"
    )
    btc_price = btc_data["Close"].iloc[-1] if not btc_data.empty else "N/A"

    return f"Gold Price: {gold_price}, BTC Price: {btc_price}"
  except Exception as e:
    return "Market data currently unavailable."


def generate_tweet():
  market_info = get_market_data()

  prompt = (
      f"Current market data: {market_info}. Act as a professional Forex,"
      " Crypto, and Stock Market analyst. Write a short, high-engagement"
      " trading analysis tweet about Gold (XAUUSD) or Bitcoin (BTC), including"
      " potential support and resistance zones, market sentiment, and a"
      " brief note on geopolitical impact if relevant. Keep it under 280"
      " characters, add relevant hashtags like #Gold #Forex #BTC, and"
      " absolutely end the tweet by promoting this Telegram channel:"
      " https://t.me/Gold_Hunter03 (Username: @Gold_Hunter03)."
  )

  response = model.generate_content(prompt)
  return response.text.strip()


def post_to_x():
  try:
    client = tweepy.Client(
        consumer_key=X_API_KEY,
        consumer_secret=X_API_SECRET,
        access_token=X_ACCESS_TOKEN,
        access_token_secret=X_ACCESS_SECRET,
    )

    tweet_text = generate_tweet()
    client.create_tweet(text=tweet_text)
    print("Tweet posted successfully!")
  except Exception as e:
    print(f"Error posting tweet: {e}")


if __name__ == "__main__":
  post_to_x()
