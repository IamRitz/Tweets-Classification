#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from urllib.parse import urlparse
import json
import csv
import time
import sys

non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

#topics = ['sports', 'science', 'politics', 'health', 'Books', 'Buisiness', 'Music', 'Fashion', 'Entertainment', 'Charity']
#topics = ['sports', 'science']
tweets = []
count = 0

#This is a basic listener that just prints received tweets to stdout.
class listener(StreamListener):

    def on_data(self, data):
        try:
            all_data = json.loads(data)
            global count
            if count >= 500:
                return False
            if not all_data["retweeted"]:
                text = all_data['text'].replace('\n', ' ')
                words = text.split()
                for i in range(len(words)):
                    r = urlparse((words[i]))
                    if r[0] != '' and r[1] != '':
                        words[i] = ""
                    
                text = ' '.join(words)
                tweets.append( [all_data['id_str'], "amazon", text] )
                count += 1
            return True
        except BaseException as e:
            print("Failed onData", str(e))

    def on_error(self, status):
        print(status)


#Variables that contains the user credentials to access Twitter API 
consumer_key = 'qw2ppzbIX29Kttc4ATnQrssoK'
consumer_secret = 'e7k8sWCPs7vpzuURu5SDLGBXI9Rhuk9XhqR2NcPDz8m3OQkURa'
access_token = '278426524-cYVjnAvEclqmeFQ2ha9uZSqvY1kVDpuGTfgq68kC'
access_token_secret = 'qx2QvxGhuON1CAd6QqLN4DLijF2bvwBuGIMPrBJKnn3Fv'


#This handles Twitter authetification and the connection to Twitter Streaming API
l = listener()
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
stream = Stream(auth, l)

#This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
#topics = ['sports', 'news', 'health', 'technology', 'politics', 'fashion']

stream.filter(languages=["en"], track=["amazon"])



print ("Writing all tweets to file ... ")
with open('finalresults2.csv', 'a', newline='') as fp:
    writer = csv.writer(fp, dialect = 'excel', delimiter=',', quotechar='', escapechar='', quoting=csv.QUOTE_NONE)
    #writer.writerow(['UserID', 'Topic', 'Tweet'])
    for tweet in tweets:
        try:
            writer.writerow(tweet)
        except:
            continue

print ("Done!")

