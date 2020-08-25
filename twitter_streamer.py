from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import twitter_credentials
import db_handler


IL_LOCATION = [34.0691, 29.3323, 35.9978, 33.4122]
IL_FILTER_1 = """country":"Israel"""
IL_FILTER_2 = """country_code":"IL"""


class TwitterStreamer():
    """
    Class for streaming and processing live tweets.
    """
    def __init__(self):
        # Variables:
        self.listener = None
        self.auth = None
        self.stream = None

    def stream_tweets(self, location_filter):
        # This handles Twitter authentication and the connection to Twitter Streaming API
        self.listener = StdOutListener()
        self.listener.set_db_client()
        self.auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
        self.auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)

        self.stream = Stream(self.auth, self.listener)
        self.stream.filter(locations=location_filter)

    def stop_stream(self):
        self.listener.stop_listen()
        self.listener.close_db_client()


# # # # TWITTER STREAM LISTENER # # # #
class StdOutListener(StreamListener):
    """
    This is a basic listener that just prints received tweets to stdout.
    """
    def __init__(self):
        super().__init__()
        self.listen = True
        self.db_client = None

    def set_db_client(self):
        self.db_client = db_handler.DBClient()
        self.db_client.connect()
        self.db_client.set_tweets_db()
        self.db_client.set_tweets_collection()

    def close_db_client(self):
        self.db_client.close()

    def on_data(self, data):
        if not self.listen:
            return False
        try:
            if IL_FILTER_1 in str(data) or IL_FILTER_2 in str(data):
                self.db_client.insert_document(data)
                print("data is: %s " % data)
                return True
        except BaseException as e:
            print("Error on on_data method: %s" % str(e))
        return True

    def on_error(self, status):
        print(status)

    def stop_listen(self):
        self.listen = False


if __name__ == '__main__':
    print("starting app.....")
    tweets_streamer = TwitterStreamer()
    tweets_streamer.stream_tweets(IL_LOCATION)
