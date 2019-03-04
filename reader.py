import numpy as np

infile = open('apple.txt', encoding='utf-8')

wordlist = open('words-list.txt', encoding='utf-8')

nn = infile.readlines()
mm = wordlist.readlines()

for line in nn:
    word = line.split(' ')
    #print(word)
    for value in mm:
        #print(value)
        if value in word:
            print(value)
