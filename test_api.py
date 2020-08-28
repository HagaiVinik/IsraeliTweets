import time

import twitter_streamer

"""
NOTE: THIS CODE IS USED ONLY FOR TESTING THE API AND SEE ITS ABILITIES.
"""


def main():
    print("starting app.....")
    # Declaring streamer and pull_tweets_client variables:
    streamer = twitter_streamer.AsyncTwitterStreamer(twitter_streamer.IL_LOCATION)
    pull_tweets_client = twitter_streamer.PullTweetsFromDB()

    # Start streaming tweets:
    pull_tweets_client.set_db_client()
    streamer.start()
    print("streamer started")
    time.sleep(1)

    # Intersection search
    param_list2 = [{'retweeted': False}, {'id': 1298946498600804352}]
    multiple_docs_2 = pull_tweets_client.get_tweets(param_list2, twitter_streamer.INTER_SEARCH)
    for doc in multiple_docs_2:
        print("doc is %s" % str(doc))

    # Unification search
    param_list = [{'id': 1298946817443401728}, {"author": "mike"}]
    multiple_docs = pull_tweets_client.get_tweets(param_list, twitter_streamer.UNI_SEARCH)
    for doc in multiple_docs:
        print("doc is %s" % str(doc))
    time.sleep(3)

    # Single search
    param = {'id': 1298946817443401728}
    single_doc = pull_tweets_client.get_tweets(param, twitter_streamer.SINGLE_SEARCH)
    print("doc is %s" % str(single_doc))
    time.sleep(3)

    # free-style search - user determines operation '$or'/ '$and'
    param = {"$or": [{'id': 1298946817443401728}, {"author": "mike"}]}
    docs = pull_tweets_client.get_tweets(param, twitter_streamer.MULTI_SEARCH)
    print("doc is %s" % str(docs))

    # let the database consume tweets for a while
    time.sleep(5)
    streamer.stop()


if __name__ == '__main__':
    main()
