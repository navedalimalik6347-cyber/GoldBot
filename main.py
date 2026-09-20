import os
import tweepy
import yfinance as yf

# API Keys setup
X_API_KEY = os.environ.get("X_API_KEY")
X_API_SECRET = os.environ.get("X_API_SECRET")
X_ACCESS_TOKEN = os.environ.get("X_ACCESS_TOKEN")
X_ACCESS_SECRET = os.environ.get("X_ACCESS_SECRET")


def get_market_analysis():
  try:
    gold = yf.Ticker("GC=F")
    btc = yf.Ticker("BTC-USD")

    gold_data = gold.history(period="1d")
    btc_data = btc.history(period="1d")

    gold_price = (
        f"{gold_data['Close'].iloc[-1]:.2f}"
        if not gold_data.empty
        else "2650.00"
    )
    btc_price = (
        f"{btc_data['Close'].iloc[-1]:.2f}"
        if not btc_data.empty
        else "65000.00"
    )

    tweet = (
        f"⚡ Market Update ⚡\n\nGold (GC): ${gold_price}\nBitcoin (BTC):"
        f" ${btc_price}\n\nKey Support & Resistance zones active. Manage your"
        " risk carefully.\n\nJoin our Telegram for daily signals & VIP setup:"
        " https://t.me/Gold_Hunter03\n\n#Gold #XAUUSD #BTC #Forex #Crypto"
        " #Gold_Hunter03"
    )
    return tweet
  except Exception as e:
    return (
        "⚡ Gold & BTC Market Update ⚡\nAnalyzing key support & resistance"
        " zones for today's session.\n\nJoin our Telegram for exclusive setups:"
        " https://t.me/Gold_Hunter03\n\n#Gold #XAUUSD #BTC #Forex #Crypto"
    )


def post_to_x():
  try:
    print("Initializing Tweepy Client...")
    client = tweepy.Client(
        consumer_key=X_API_KEY,
        consumer_secret=X_API_SECRET,
        access_token=X_ACCESS_TOKEN,
        access_token_secret=X_ACCESS_SECRET,
    )

    tweet_text = get_market_analysis()
    print(f"Generated Tweet:\n{tweet_text}")

    response = client.create_tweet(text=tweet_text)
    print(f"Tweet posted successfully! Response: {response}")
  except Exception as e:
    print(f"CRITICAL ERROR posting tweet: {e}")
    raise e


if __name__ == "__main__":
  post_to_x()
