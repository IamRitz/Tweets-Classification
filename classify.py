from collections import Counter, defaultdict
from math import log
import re
import random
import csv


fp = open('apple_with_cond_prob.csv', 'r', encoding='utf-8')
reader = csv.reader(fp)
priors['apple'] = 

def tokenize(text):
    """break the text into words"""
    return re.findall('[a-z0-9]+', text)

def read_training_file(filename):
    priors = Counter()
    likelihood = defaultdict(Counter)

    """
    with open(filename, encoding='utf-8') as f:
        for line in f:
            parts = line.split(',')
            priors[parts[1]] += 1
            for word in tokenize(parts[2]):
                likelihood[parts[1]][word] += 1
    """

    wi
    return (priors, likelihood)

def classify(line, priors, likelihood):
    """ return a random category"""
    categories = priors
    return categories[int(random.random() * len(categories))]

def classify_max_prior(line, priors, likelihood):
    return max(priors, key=lambda x:priors[x])

def classify_bayesian(line, priors, likelihood):
    max_class = (-1E6, '')
    for c in priors.keys():
        p = priors[c]
        n = float(sum(likelihood[c].values()))
        for word in tokenize(line[2]):
            p = p * max(1E-6, likelihood[c][word] / n)

        if p > max_class[0]:
            max_class = (p, c)

    return max_class[1]

def read_testing_file(filename):
    return [line.strip().split(',') for line in open(filename, encoding='utf-8').readlines()]

def main():
    training_file = 'train_data.csv'
    testing_file = 'test_data.csv'

    [priors, likelihood] = read_training_file(training_file)
    lines = read_testing_file(testing_file)

    num_correct = 0
    for line in lines:
        if classify_bayesian(line, priors, likelihood) == line[1]:
            num_correct += 1
    print("Classified %d correctly out of %d for an accuracy of %f"%(num_correct, len(lines), float(num_correct)/len(lines)))     
if __name__ == '__main__':
    main()
