import os
import csv
import nltk, re
#from urllib import urlopen
#from string import lower
from nltk.corpus import wordnet

_c =    "[^aeiou]"          # consonant
_v =    "[aeiouy]"          # vowel
_C =    _c + "[^aeiouy]*"    # consonant sequence
_V =    _v + "[aeiou]*"      # vowel sequence

Mgre0 = re.compile("^(" + _C + ")?" + _V + _C)               # [C]VC... is m>0
Meq1 = re.compile("^(" + _C + ")?" + _V + _C +"(" + _V + ")"+ "?" + "$")  # [C]VC[V] is m=1
Mgre1 = re.compile("^(" + _C + ")?" + _V + _C + _V + _C)        # [C]VCVC... is m>1
CVCending = re.compile(_C + _v + "[^aeiouwxy]$")
vstem   = re.compile("^(" + _C + ")?" + _v)                   # vowel in stem
DoubleConsonant=  re.compile(r"([^aeiouylsz])\1$")   #matches double consonants excpet l s and z
removeEndingPunc  =  re.compile(r"[^a-z]+$")


def clean_html(html, remove_entities=False):
    p = re.compile("<(script|style).*?>.*?</(script|style)>", re.DOTALL)
    cleaned = re.sub(p, "", html)               # remove inline js/css
    cleaned = re.sub("<(.|\n)*?>", "", cleaned) # remove remaining html tags
    if remove_entities: cleaned = re.sub("&[^;]*; ?", "", cleaned)
    return cleaned

def stem(parms):
    stems = []
    for word in parms:

        ######## step 0               pre-process words
        word = word.lower()
        word = re.sub(removeEndingPunc,"",word)

        if len(word) < 3:            # don't stem if word smaller than 3
            stems.append(word)
            continue
        if word[0] == 'y': word = 'Y' + word[1:]      # make sure initial Y is not considered a vowel


        if word[-1] == 's' and word[-2] != 's':
            if word[-4:] == 'sses':
                word = word[:-4] + 'ss'
            elif word[-3:] == 'ies':
                word = word[:-3] +  'i'
            else:
                word = word[:-1]

        flag = None                         # only set to 1 2nd and 3rd steps are taken
        if word[-3:] == 'eed':                    # m>0   eed -> ee
            if Mgre0.search(word[:-3]):
                word = word[:-3] + "ee"

        elif word[-2:] == 'ed':                   # *v* ed
            if vstem.search(word[:-2]):
                word = word[:-2]
                flag = 1
        elif word[-3:] == 'ing':                  # *v* ing
            if vstem.search(word[:-3]):
                word = word[:-3]
                flag = 1

        if flag:                                                # go on to part 1b2
            if word[-2:] == 'at':                               # at -> ate
                word = word[:-2] + 'ate'
            elif word[-2:] == 'bl':                             
                word = word[:-2] + 'ble'
            elif word[-2:] == 'iz':                             
                word = word[:-2] + 'ize'
            elif DoubleConsonant.search(word):                 
                word = word[:-1]                                
            elif CVCending.search(word) and Meq1.search(word): 
                word = word + 'e'                               # add an e


        if word != '':
        #if not wordnet.synsets(word):
            stems.append(word)

    return stems



#files = ['apple.txt', 'google.txt', 'microsoft.txt', 'twitter.txt']

#for file in files:
file = 'twitter.txt'
fo = open(file, encoding="utf-8")

nn = fo.readlines()
#nn = applef.readlines()

# Close open file
fo.close()
# We remove the symbol hashtag
cleanText= []
for x in nn:
    s = list(x)
    for i in range(1,len(s)):
        if s[i] == "#":
            s[i] = " "

    cleanText.append("".join(s))

# We tokenize (list of words)
cleanText = "".join(cleanText)
cleanText = nltk.word_tokenize(cleanText)

cleanText = [w.lower() for w in cleanText]
bad = ["null","true","false","width","http","height","length","type","u.","false",'option','acest']

filtered_words = [w for w in cleanText if len(w) >=  4]
filtered_words = [w for w in filtered_words if w not in bad]
filtered_words = [w for w in filtered_words if w not in nltk.corpus.stopwords.words('english')]
filtered_words = [w for w in filtered_words if wordnet.synsets(w)]

final = stem(filtered_words)

words_list = []

"""
with open("wordsonly3.txt", 'a') as f:
    for s in final:
        if s not in words_list:
            words_list.append(s)
            if s != 'http':
                f.write(s + '\n')
    #f.write('\n')
"""
