import tweepy
from tweepy import OAuthHandler
import sys
import csv
import unicodedata
from urllib.parse import urlparse
import json
import jsonpickle

consumer_key = 'qw2ppzbIX29Kttc4ATnQrssoK'
consumer_secret = 'e7k8sWCPs7vpzuURu5SDLGBXI9Rhuk9XhqR2NcPDz8m3OQkURa'
access_token = '278426524-cYVjnAvEclqmeFQ2ha9uZSqvY1kVDpuGTfgq68kC'
access_secret = 'qx2QvxGhuON1CAd6QqLN4DLijF2bvwBuGIMPrBJKnn3Fv'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

if (not api):
    print("Can't Authenticate")
    sys.exit(-1)

#qfile = open('queries.txt', 'r')
qfile = ['Charity']*10
topics = ['sports', 'science', 'politics', 'health', 'Books', 'Business', 'Music', 'Fashion', 'Charity']

tweetsPerQry = 100
fName = 'tweetsfinal4.csv'
sinceId = None
maxTweets = 1000
max_id = -1
tweets = []
tweetCount = 0
print("Downloading max {0} tweets".format(maxTweets))

for searchQuery in qfile:
    try:
        if (max_id <= 0):
            if (not sinceId):
                new_tweets = api.search(q=searchQuery, count=tweetsPerQry)
            else:
                new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                        since_id=sinceId)
        else:
            if (not sinceId):
                new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                        max_id=str(max_id - 1))
            else:
                new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                        max_id=str(max_id - 1),
                                        since_id=sinceId)
        if not new_tweets:
            print("No more tweets found")
            break
        for line in new_tweets:
            value = jsonpickle.encode(line._json, unpicklable=False)
            tweet = json.loads(value)
            if not tweet["retweeted"]:
                text = (tweet['text'].replace('\n', ' '))
                """
                words = text.split()  # remove URLs
                for i in range(len(words)):
                        r = urlparse(words[i])
                    if r[0] != '' and r[1] != '':
                        words[i] = ""
                        
                text = ' '.join(words).encode('utf-8')
                """
                t = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode("utf-8")
                tweets.append([searchQuery, tweet['id_str'], t])
                # f.write(jsonpickle.encode(tweet._json, unpicklable=False) +
                #      '\n')
        tweetCount += len(new_tweets)
        print("Downloaded {0} tweets".format(tweetCount))
        max_id = new_tweets[-1].id
    except tweepy.TweepError as e:
        # Just exit if any error
        print("some error : " + str(e))
        break

print("Downloaded {0} tweets, Saved to {1}".format(tweetCount, fName))

print("Writing all tweets to file ... ")
tfile = open(fName, 'a', encoding='utf-8', newline='')
writer = csv.writer(tfile, dialect = 'excel', delimiter=',', quotechar='"', escapechar='\\', quoting=csv.QUOTE_ALL)
for tweet in tweets:
    writer.writerow(tweet,)
print("Done!")
