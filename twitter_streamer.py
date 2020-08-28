import threading

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import twitter_credentials
import db_handler


# this is according to: www.boundingbox.klokantech.com
IL_LOCATION = [34.0691, 29.3323, 35.9978, 33.4122]
IL_FILTER_1 = """country":"Israel"""
IL_FILTER_2 = """country_code":"IL"""

# Search Types:
SINGLE_SEARCH = "single_search"
MULTI_SEARCH = "multi_search"
UNI_SEARCH = "uni_search"
INTER_SEARCH = "inter_search"


class PullTweetsFromDB():
    def __init__(self):
        self.db_client = None

    def set_db_client(self):
        self.db_client = db_handler.DBClient()
        self.db_client.connect()
        self.db_client.set_tweets_db()
        self.db_client.set_tweets_collection()

    def get_tweets(self, param, search_type):
        if search_type == SINGLE_SEARCH:
            return self.db_client.find_single_document(param)
        elif MULTI_SEARCH == search_type:
            return self.db_client.find_documents(param)
        elif search_type == UNI_SEARCH:
            updated_param = {"$or": param}
            return self.db_client.find_documents(updated_param)
        elif search_type == INTER_SEARCH:
            updated_param = {"$and": param}
            return self.db_client.find_documents(updated_param)


class AsyncTwitterStreamer(threading.Thread):
    def __init__(self, location_filter):
        threading.Thread.__init__(self)
        self.location_filter = location_filter
        self.ts = TwitterStreamer()

    def run(self):
        self.ts.stream_tweets(self.location_filter)

    def stop(self):
        self.ts.stop_stream()


class TwitterStreamer():
    """
    Class for streaming and processing live tweets.
    """
    def __init__(self):
        # Variables:
        self.listener = None
        self.auth = None
        self.stream = None
        self.tweets_thread = None

    def start_streaming_tweets(self):
        self.tweets_thread = threading.Thread(target=self.stream_tweets)
        self.tweets_thread.start()

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


class StdOutListener(StreamListener):
    """
    This is a listener that writes/reads tweets from database.
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

    def on_data(self, data):    # Callback method
        if not self.listen:
            return False
        try:
            if IL_FILTER_1 in str(data) or IL_FILTER_2 in str(data):
                self.db_client.insert_document(data)
                return True
        except BaseException as e:
            print("Error on on_data method: %s" % str(e))
        return True

    def on_error(self, status):     # Callback method
        print(status)

    def stop_listen(self):      # Callback method
        self.listen = False
