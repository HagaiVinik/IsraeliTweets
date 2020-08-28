# IsraeliTweets

IsraeliTweets is a used for listening to all tweets that were made in Israel

# Features:

  - Listening to all tweets that were created in Israel.
  - handles API requests.


You need to have the following packages installed:
  - tweepy
  - pymongo 

Also you need to have Mongodb software installed and ready to use. 

### Set a Mongodb with this details:
MONGO_HOST = 'mongodb://localhost/israeli_tweets'

NAME OF DB - israeli_tweets

NAME OF COLLECTION - tweets

    
# API PROTOCOL:
## Documentation for drawing documents from database.
    
##SINGLE DOCUMENT:
if you want to look for a single document,the parameter that you are passing should be a dict. 
it is important to check your keys and values types, and enter them correctly for getting your desired document. 

##### example:   
param = {'id': 1298946817443401728}


## MULTIPLE DOCUMENTS 
#### OPTION 1: INTER_SEARCH - CONTAINING ALL PARAMETERS
#### OPTION 2: UNI_SEARCH - CONTAINING AT LEAST ONE PARAMETER
if you want to look for a many documents, the parameter that you are passing should be a list with
dict parameters inside it.
it is important to check your keys and values types, and enter them correctly, for getting your desired documents.

##### example: 
param = [{'id': 1298946817443401728}, {'id_str': '2735258479'} ]


## Code Example:
### ( see test_api for more details )


import  twitter_streaming

def main():

    print("starting app.....")]
    
    # Declaring streamer and pull_tweets_client variables:
    streamer = twitter_streamer.AsyncTwitterStreamer(twitter_streamer.IL_LOCATION)
    pull_tweets_client = twitter_streamer.PullTweetsFromDB()

    # Start streaming tweets:
    pull_tweets_client.set_db_client()
    streamer.start()
    print("streamer started")
    
    # let the database consume tweets for a while
    time.sleep(15)
    streamer.stop()


if __name__ == '__main__':
    main()

