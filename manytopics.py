from urllib.parse import urlparse
from tweepy import *
import csv
import json
import time

class listener(StreamListener):

    def on_data(self, data):
        try:
            all_data = json.loads(data)
        if count >= 10
            return True
        except BaseException as e:
            print("Failed onData", str(e))
            time.sleep(5)

    def on_error(self, status):
        print(status)

# initialize some variables
topics = ['sports', 'science', 'politics', 'health', 'Books', 'Buisiness', 'Music', 'Fashion', 'Entertainment', 'Charity']
tweets = []

consumer_key = 'qw2ppzbIX29Kttc4ATnQrssoK'
consumer_secret = 'e7k8sWCPs7vpzuURu5SDLGBXI9Rhuk9XhqR2NcPDz8m3OQkURa'
access_token = '278426524-cYVjnAvEclqmeFQ2ha9uZSqvY1kVDpuGTfgq68kC'
access_token_secret = 'qx2QvxGhuON1CAd6QqLN4DLijF2bvwBuGIMPrBJKnn3Fv'

l = listener()

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
stream = Stream(auth, l)

# getting tweets
for topic in topics:
    iterator = stream.filter(languages=['en'], track=topic)
    print(iterator)
    time.sleep(5)
    count = 0
    print ("Getting tweets for topic: " + topic + " ...")
    
    for tweet in iterator:
        if count >= 1000:
            break

        # Removing the retweets
        if not tweet["retweeted"]:
            text = tweet['text'].replace('\n', ' ')

            # removing the URLs
            words = text.split()
            for i in range(len(words)):
                r = urlparse((words[i]))
                if r[0] != '' and r[1] != '':
                    words[i] = ""
                    
            text = ' '.join(words).encode('utf-8')
            tweets.append( [tweet['id_str'], topic, text] )
            count += 1

# writing tweets to file
print ("Writing all tweets to file ... ")
tfile = open('newtweets.csv', 'a', newline='')
writer = csv.writer(tfile, delimiter=',', quotechar='"', escapechar='\\', quoting=csv.QUOTE_ALL)
writer.writerow(['UserID', 'Topic', 'Tweet'])
for tweet in tweets:
    writer.writerow(tweet)
print ("Done!")
