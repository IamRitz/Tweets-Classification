"""Stemming the given line"""
import re

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
