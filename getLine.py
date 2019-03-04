import sys
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
#files = ['apple.txt', 'google.txt', 'microsoft.txt', 'twitter.txt']

def main():
    #number_of_lines(file)
    print('Get the no of documents in one category')

def number_of_lines(file):
    """
    count = [0, 0, 0, 0]
    i = 0
    for file in files:
        fo = open(file, encoding='utf-8')
        rl = fo.readlines()
        for line in rl:
            count[i] += 1
        i += 1
    fo.close()
    """
    count = 0
    fo = open(file, encoding='utf-8')
    rl = fo.readlines()
    for line in rl:
        count += 1
    print(count)
    #print(sum(count))


if __name__ == '__main__':
    main()
