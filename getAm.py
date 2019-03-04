import json
import unicodedata

fp = open("all_tweets_amazon.txt", 'r', encoding="utf-8")

my_dict = dict()
for i in fp:
    my_dict = json.loads(i)
    value = my_dict['text']
    print((unicodedata.normalize('NFKD', all_data['text']).encode('ascii', 'ignore')).decode('utf-8'))
