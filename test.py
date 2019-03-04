"""
from sklearn.feature_extraction.text import CountVectorizer


corpus = [
'All my cats in a row',
'When my cat sits down, she looks like a Furby toy!',
'The cat from outer space',
'Sunshine loves to sit like this for some reason.'
]

#corpus = open('wordsonly2.txt', encoding='utf')

vectorizer = CountVectorizer()
print( vectorizer.fit_transform(corpus).todense() )
print( vectorizer.vocabulary_ )
"""

import csv
import sys
count = 0
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
#print(x.translate(non_bmp_map))

file = open('finalresults.csv', encoding='utf-8')

reader = csv.reader(file)

fp = open('apple_train.txt', 'w')
for row in reader:
    count += 1
    if count == 700:
        break
    fp.write(row[2].translate(non_bmp_map))
