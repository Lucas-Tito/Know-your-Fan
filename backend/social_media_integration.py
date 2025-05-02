import tweepy
from instagram_private_api import Client
from twitchAPI.twitch import Twitch

class SocialMediaIntegration:
    def __init__(self):
        # Twitter API setup
        self.twitter_auth = tweepy.OAuthHandler(
            "TWITTER_API_KEY",
            "TWITTER_API_SECRET"
        )
        self.twitter_api = tweepy.API(self.twitter_auth)

        # Instagram API setup
        self.instagram_api = Client(
            "INSTAGRAM_USERNAME",
            "INSTAGRAM_PASSWORD"
        )

        # Twitch API setup
        self.twitch = Twitch("TWITCH_CLIENT_ID", "TWITCH_CLIENT_SECRET")

    def get_twitter_data(self, username):
        try:
            user = self.twitter_api.get_user(screen_name=username)
            tweets = self.twitter_api.user_timeline(screen_name=username, count=100)

            # Análise dos tweets relacionados a esports
            esports_tweets = [
                tweet for tweet in tweets
                if any(keyword in tweet.text.lower()
                      for keyword in ['furia', 'csgo', 'valorant', 'esports'])
            ]

            return {
                "following_count": user.friends_count,
                "esports_tweets": len(esports_tweets),
                "total_tweets": len(tweets)
            }
        except Exception as e:
            return {"error": str(e)}