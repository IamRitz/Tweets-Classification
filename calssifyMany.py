from collections import Counter, defaultdict
import math
import re
from urllib.parse import urlparse
import random
import csv
import matplotlib.pyplot as plt
import time
import nltk
from stemming import stem
import sys
import unicodedata
#ISO-8859-1
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
cat_correct = {'sports':0, 'science':0, 'politics':0, 'health':0, 'Books':0, 'Business':0, 'Music':0, 'Fashion':0, 'Charity':0}
topics = ['sports', 'science', 'politics', 'health', 'Books', 'Business', 'Music', 'Fashion', 'Charity']
cat_length = {'sports':0, 'science':0, 'politics':0, 'health':0, 'Books':0, 'Business':0, 'Music':0, 'Fashion':0, 'Charity':0}

def tokenize(text):
    """break the text into words"""
    cleanText = []
    filtered_words = []
    for x in text:
        s = list(x.lower())
        for i in range(len(s)):
            if s[i] == "#":
                s[i] = " "

        cleanText.append("".join(s))
    
    cleanText = "".join(cleanText)
    words = cleanText.split()
    for i in range(len(words)):
        r = urlparse((words[i]))
        if r[0] != '' and r[1] != '':
            words[i] = ""
        
    cleanText = ' '.join(words)
    cleanText = nltk.word_tokenize(cleanText)
    
    bad = ["null","true","false","http","u."]

    filtered_words = [w for w in cleanText if len(w) >=  4]
    filtered_words = [w for w in filtered_words if w not in bad]
    filtered_words = [w for w in filtered_words if w not in nltk.corpus.stopwords.words('english')]
    filtered_words = [w for w in filtered_words if nltk.corpus.wordnet.synsets(w)]
    #return re.findall('[a-z0-9]+', cleanText)
    #filtered_words = stem(filtered_words)
    return filtered_words

def read_training_file(filename):
    priors = Counter()
    likelihood = defaultdict(Counter)
    with open(filename, encoding='utf-8') as f:
        for line in f:
            parts =line.split(',')
            if len(parts) == 3:
                priors[parts[0]] += 1
                for word in tokenize(parts[2]):
                    likelihood[parts[0]][word] += 1
    print("Priors: \n", priors.most_common())
    #print(likelihood)

    return (priors, likelihood)

def classify(line, priors, likelihood):
    """ return a random category """
    categories = list(priors.keys())
    return categories[int(random.random() * len(categories))]

def classify_max_prior(line, priors, likelihood):
    return max(priors, key=lambda x:priors[x])

def classify_bayesian_with_zero_fix(line, priors, likelihood):
    """ Using the bayes theorem """
    max_class = (-1E6, '')
    for c in priors.keys():
        p = priors[c]
        n = float(sum(likelihood[c].values()))
        for word in tokenize(line[2]):
            #print("Con. Prob of %s in %s: %f"%(word, c, (max(1E-6, likelihood[c][word] / n))))
            #time.sleep(1)
            p = p * max(1E-6, likelihood[c][word] / n)
        #print(p)
        #time.sleep(5)
        if p > max_class[0]:
            max_class = (p, c)

    return max_class[1]
def classify_bayesian(line, priors, likelihood):
    """ Using the bayes theorem """
    max_class = (-1E6, '')
    for c in priors.keys():
        p = priors[c]
        n = float(sum(likelihood[c].values()))
        for word in tokenize(line[2]):
            p = p * (likelihood[c][word] / n)

        if p > max_class[0]:
            max_class = (p, c)

    return max_class[1]

def read_testing_file(filename):
    filtered = [line.strip().split(',')for line in open(filename, encoding='utf-8').readlines()]
    return filtered
    #return [line.strip().split(',')for line in open(filename, encoding='utf-8').readlines()]

def main():
    global cat_correct
    global cat_length
    training_file = 'train_dataNEW.csv'
    testing_file = 'test_dataNEW.csv'

    [priors, likelihood] = read_training_file(training_file)
    lines = read_testing_file(testing_file)

    num_correct = [0, 0, 0, 0]
    accuracy = [0, 0, 0, 0]
    num_c = 0

    for line in lines:
        cat_length[line[0].replace('"', '')] += 1
        try:
            cat = classify_bayesian_with_zero_fix(line, priors, likelihood)
            if classify(line, priors, likelihood) == line[0]:
                num_correct[0] += 1
            if classify_max_prior(line, priors, likelihood) == line[0]:
                num_correct[1] += 1
            if classify_bayesian(line, priors, likelihood) == line[0]:
                num_correct[2] += 1

            if classify_bayesian_with_zero_fix(line, priors, likelihood) == line[0]:
                cat_correct[line[0].replace('"', '')] += 1
                num_correct[3] += 1
            #print(line[2], ':', cat)
                #num_c += 1
                #time.sleep(1)
        
        except Exception as e:
            print("Error Occured: ", str(e))
            continue
 
    accuracy[0] =  float(num_correct[0])/len(lines) * 100
    accuracy[1] =  float(num_correct[1])/len(lines) * 100
    accuracy[2] =  float(num_correct[2])/len(lines) * 100
    accuracy[3] =  float(num_correct[3])/len(lines) * 100
    
    print("Random Classify: Classified %d correctly out of %d for an accuracy of %f \n"%(num_correct[0], len(lines), accuracy[0]))
    print("Max_prior: Classified %d correctly out of %d for an accuracy of %f \n"%(num_correct[1], len(lines), accuracy[1]))
    print("Naive_bayes: Classified %d correctly out of %d for an accuracy of %f \n"%(num_correct[2], len(lines), accuracy[2]))
    print("Naive_Bayes(with zero fix) : Classified %d correctly out of %d for an accuracy of %f\n"%(num_correct[3], len(lines), accuracy[3]))
    print("Category wise Output of Testing file: \n", cat_correct)
    print("Total no of categories testing file \n", cat_length)
    print("Category wise Accuracy: \n", [i/j for i, j in zip(cat_correct.values(), cat_length.values())])
    
    x = [1, 2, 3, 4]
    my_ticks = ['Random', 'Max_prior', 'Bayesian', 'Bayesian(zero fix)']
    plt.plot(x, accuracy, label = 'Classification Curve')
    #plt.bar(x, accuracy, label = 'Classification Bar')
    plt.xticks(x, my_ticks)
    plt.xlabel('Classification Approach')
    plt.ylabel('Accuracy found in percentage(%)')
    plt.legend()
    plt.show()

if __name__ == '__main__':
    main()
