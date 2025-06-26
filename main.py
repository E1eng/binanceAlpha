import requests
import snscrape.modules.twitter as sntwitter

# Konfigurasi
TELEGRAM_BOT_TOKEN = "7886680680:AAHeCLXFC-9WiofvK34WaeP55c_Qa5XVg5M"
TELEGRAM_CHAT_ID = "1002242723919"
LAST_TWEET_FILE = "last_tweet_id.txt"

def get_last_tweet_id():
    try:
        with open(LAST_TWEET_FILE, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

def save_last_tweet_id(tweet_id):
    with open(LAST_TWEET_FILE, "w") as f:
        f.write(tweet_id)

def scrape_tweets():
    tweets = []
    for tweet in sntwitter.TwitterUserScraper("binance").get_items():
        if tweet.lang != "en":
            continue
        tweets.append({
            "id": tweet.id,
            "content": tweet.content
        })
        if len(tweets) >= 5:
            break
    return tweets

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "disable_web_page_preview": False
    }
    requests.post(url, data=payload)

def main():
    last_id = get_last_tweet_id()
    tweets = scrape_tweets()
    new_tweets = []

    for tweet in tweets:
        if last_id and str(tweet["id"]) <= last_id:
            continue
        content_lower = tweet["content"].lower()
        if "binance alpha" in content_lower and "feature" in content_lower:
            new_tweets.append(tweet)

    new_tweets.sort(key=lambda x: x["id"])  # urutkan dari lama ke baru
    for tweet in new_tweets:
        msg = f"🚨 New Tweet from @binance:\n\n{tweet['content']}\n\n🔗 https://twitter.com/binance/status/{tweet['id']}"
        send_to_telegram(msg)
        save_last_tweet_id(str(tweet["id"]))

if __name__ == "__main__":
    main()
    
