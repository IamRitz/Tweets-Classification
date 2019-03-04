import json
import unicodedata

tweets = open('tweets1.txt', 'r')
output = open('textonly2.txt', 'w')

my_dict = dict()
for item in tweets:
    my_dict = json.loads(item)
    value = my_dict['text']
    output.write((unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')).decode('utf-8') + '\n')







