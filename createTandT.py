import csv
import time
import sys
import codecs

fp = open('tweetsfinal4.csv', encoding='utf-8')
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
reader = csv.reader(fp)

train_results = codecs.open('train_dataNEW.csv', 'a', encoding='utf-8', errors='ignore')
writerTrain = csv.writer(train_results, dialect = 'excel', delimiter=',', quotechar='"', escapechar='\\', quoting=csv.QUOTE_ALL)
test_results = codecs.open('test_dataNEW.csv', 'a', encoding='utf-8', errors='ignore')
writerTest= csv.writer(test_results, dialect = 'excel', delimiter=',', quotechar='"', escapechar='\\', quoting=csv.QUOTE_ALL)

appletrncount = 0
#appletstcount = 0
googletrncount = 0
#googletstcount = 0
microsofttrncount = 0

twittertrncount = 0

amazoncount = 0
b = c = m = 0
fashion = 0
for i in reader:
    if i[0] == 'sports':
        if appletrncount <= 800:
            writerTrain.writerow(i)
        elif appletrncount >800 and appletrncount <= 1144:
            writerTest.writerow(i)
        appletrncount += 1
    if i[0] == 'science':
        if googletrncount <= 670:
            writerTrain.writerow(i)
        elif googletrncount > 670 and googletrncount <= 956:
            writerTest.writerow(i)
        googletrncount += 1
    if i[0] == 'politics':
        if microsofttrncount <= 670:
            writerTrain.writerow(i)
        elif microsofttrncount > 670 and microsofttrncount <= 957:
            writerTest.writerow(i)
        microsofttrncount += 1
    if i[0] == 'health':
        if twittertrncount <= 685:
            writerTrain.writerow(i)
        elif twittertrncount > 685 and twittertrncount <= 979:
            writerTest.writerow(i)
        twittertrncount += 1
    if i[0] == 'Books':
        if amazoncount <= 660:
            writerTrain.writerow(i)
        elif amazoncount > 660 and amazoncount <= 943:
            writerTest.writerow(i)
        amazoncount += 1
    if i[0] == 'Business':
        if b <= 665:
            writerTrain.writerow(i)
        elif b > 665 and b <= 950:
            writerTest.writerow(i)
        b += 1
    if i[0] == 'Music':
        if m <= 684:
            writerTrain.writerow(i)
        elif m > 684 and m <= 977:
            writerTest.writerow(i)
        m += 1
    if i[0] == 'Charity':
        if c <= 667:
            writerTrain.writerow(i)
        elif c > 667 and c <= 953:
            writerTest.writerow(i)
        c += 1
    if i[0] == 'Fashion':
            if fashion <= 640:
                writerTrain.writerow(i)
            elif fashion > 640 and fashion <= 913:
                writerTest.writerow(i)
            fashion += 1


#print(i[0])
#time.sleep(2)

