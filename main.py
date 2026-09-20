import os
import yfinance as yf
import tweepy
from google import genai

# 1. Initialize Gemini Client (Using standard modern SDK)
gemini_api_key = os.environ.get("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable is missing!")

client_ai = genai.Client(api_key=gemini_api_key)

def get_market_data():
    """Fetches Gold (GC=F) and Bitcoin (BTC-USD) prices safely."""
    gold_price = "N/A"
    btc_price = "N/A"
    
    try:
        # Fetch Gold
        gold = yf.Ticker("GC=F")
        gold_data = gold.history(period="1d")
        if not gold_data.empty:
            gold_price = f"${gold_data['Close'].iloc[-1]:.2f}"
    except Exception as e:
        print(f"Error fetching Gold data: {e}")

    try:
        # Fetch Bitcoin
        btc = yf.Ticker("BTC-USD")
        btc_data = btc.history(period="1d")
        if not btc_data.empty:
            btc_price = f"${btc_data['Close'].iloc[-1]:.2f}"
    except Exception as e:
        print(f"Error fetching Bitcoin data: {e}")

    return gold_price, btc_price

def generate_tweet_text(gold_price, btc_price):
    """Generates engaging trading analysis tweet using Gemini."""
    prompt = f"""
    Create a professional, short financial market update tweet for Gold (GC) and Bitcoin (BTC).
    Current Prices:
    - Gold (GC): {gold_price}
    - Bitcoin (BTC): {btc_price}
    
    Include brief professional market sentiment, risk management note, and promote this Telegram channel for daily signals and VIP setup: https://t.me/Gold_Hunter03
    Add relevant hashtags like #Gold #XAUUSD #BTC #Forex #Crypto #Gold_Hunter03.
    Keep it within 280 characters, punchy, and engaging.
    """
    
    try:
        # Using the standard gemini-2.5-flash or stable model configuration
        response = client_ai.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        return response.text
    except Exception as e:
        print(f"Gemini generation error: {e}, falling back to default text.")
        # Fallback template if AI generation fails
        return (
            f"⚡ Market Update ⚡\n\n"
            f"Gold (GC): {gold_price}\n"
            f"Bitcoin (BTC): {btc_price}\n\n"
            f"Key Support & Resistance zones active. Manage your risk carefully.\n\n"
            f"Join our Telegram for daily signals & VIP setup: https://t.me/Gold_Hunter03\n\n"
            f"#Gold #XAUUSD #BTC #Forex #Crypto #Gold_Hunter03"
        )

def post_to_x():
    """Authenticates with X API (OAuth 1.0a) and posts the tweet."""
    api_key = os.environ.get("X_API_KEY")
    api_secret = os.environ.get("X_API_SECRET")
    access_token = os.environ.get("X_ACCESS_TOKEN")
    access_secret = os.environ.get("X_ACCESS_SECRET")

    if not all([api_key, api_secret, access_token, access_secret]):
        raise ValueError("One or more X (Twitter) API credentials are missing in Environment Secrets!")

    print("Initializing Tweepy Client...")
    client = tweepy.Client(
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_secret
    )

    # Fetch Data
    gold_price, btc_price = get_market_data()
    
    # Generate Tweet
    tweet_text = generate_tweet_text(gold_price, btc_price)
    print("Generated Tweet:\n")
    print(tweet_text)
    print("-" * 40)

    try:
        response = client.create_tweet(text=tweet_text)
        print(f"Successfully posted to X! Tweet ID: {response.data['id']}")
    except Exception as e:
        print(f"CRITICAL ERROR posting tweet: {e}")
        raise e

if __name__ == "__main__":
    post_to_x()
