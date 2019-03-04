import csv

apple = open("apple.txt", "w")
count = 0

with open("tweets.csv", 'r') as csvfile:
    content = csv.reader(csvfile)
    for row in content:
        if count == 0:
            count += 1
            continue
        else:
            apple.write(row[0] + '\n')
