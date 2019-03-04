from textprocess import tokenizer
from textprocess import normalizer
from textprocess import stopwordremover
from textprocess import stemmer


input = 'apple.txt'

tokenized = tokenizer.tokenize(input, readFile=True)
normalized = []
for value in tokenized:
    normalized.append(normalizer.normalize(value))


#filtered = stemmer.lemmatize(filtered,cascade=False)
filtered = []
for value in normalized:
    filtered.append(stopwordremover.remove_stop_word(value))
    
stemmerfil = []
for value in filtered:
    stemmerfil.append(stemmer.lemmatize(value,cascade=False))


outfile = open('vocab.txt', 'w')
for value in stemmerfil:
    for item in value:
        outfile.write(item + '\n')
