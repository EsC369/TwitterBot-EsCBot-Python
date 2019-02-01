
import tweepy
import time
from keys import *     # NOTE: keys are in the keys.py to separate them


# Access Twitter APi:
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# call file name for storing id (only for no data base)
FILE_NAME = 'last_seen_id.txt'

# Define all tweet content into variable mentions:
# mentions = api.mentions_timeline()

# # Live Functions:---

def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id

def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return

def reply_to_tweets():
    count = 0
    print('retrieving and replying to tweets...')

    # DEV NOTE: use 1090436206926524416 for testing.
    last_seen_id = retrieve_last_seen_id(FILE_NAME)

    # NOTE: We need to use tweet_mode='extended' below to show all full tweets (with full_text). Without it, long tweets would be cut off.
    mentions = api.mentions_timeline(last_seen_id)

    for mention in reversed(mentions):   # reverse list
        # print(str(mention.id) + ' - ' + mention.text)
        last_seen_id = mention.id
        store_last_seen_id(last_seen_id, FILE_NAME)
        if '#hellobro!' in mention.text.lower():  # if #helloworld was mentioned, then 
            print('found #hellobro!')
            print('responding back...')
            try:
                    count = count + 1
                    api.update_status('@' + mention.user.screen_name + ' Hello bro! back to you! Number '+ str(count), mention.id)
                    print("Bot Message Scan And Responding Complete!")
            except tweepy.error.TweepError:
                    print("Encountered error? Passing, no responses sent")
                #     api.update_status('@' + mention.user.screen_name + ' Hello bro! back to you!', mention.id)
                #     print("Bot Message Scan And Responding Complete!")
                    pass

# End of functions------------

while True:
    reply_to_tweets()
    time.sleep(30) # Checks every 30 seconds