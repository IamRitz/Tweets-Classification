from collections import OrderedDict

with open('wordsonly3.txt') as fin:
    lines = (line.rstrip() for line in fin)
    unique_lines = OrderedDict.fromkeys( (line for line in lines if line) )



fp = open('realwordsonly.txt', 'w')
for word in unique_lines.keys():
    fp.write(word + '\n')
