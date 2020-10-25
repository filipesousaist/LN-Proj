from const import ALL_UPPER
from sys import argv

#W1, W2, W3 = argv[4:7]

def countOccurrences(tokens, occurrences, weight=1):
    length = len(tokens)
    for word in tokens:
        countWord(word, occurrences, weight)
        if word.isupper():
            length += 1
            countWord(ALL_UPPER, occurrences, weight)
    return length

def countStart(tokens, occurrences, weight=1):
    countWord('@,' + tokens[0].lower(), occurrences, weight)

def countBigrams(tokens, occurrences, weight=1):
    tokens = ['@'] + tokens + ['@']
    
    for i in range(0, len(tokens) - 1):
        countWord(tokens[i].lower() + ',' + tokens[i+1].lower(), occurrences, weight)
    
    return len(tokens) - 1

def countTrigrams(tokens, occurrences, weight=1):
    tokens = ['@'] + tokens #+ ['@']
    
    for i in range(0, len(tokens) - 2):
        countWord(tokens[i].lower() + ',' + 
                  tokens[i+1].lower() + ',' + 
                  tokens[i+2].lower(),
            occurrences, weight)
    
    return len(tokens) - 2

def countDistantBigrams(tokens, occurrences, weight=1):
    for d in range(2, len(tokens)):
        for i in range(0, len(tokens) - d):
            countWord(tokens[i].lower() + ',,' +
                      tokens[i + d].lower(),
                occurrences, weight)
                    

def countQuadrigrams(tokens, occurrences, weight=1):
    if len(tokens) == 0:
        return 0

    tokens = ['@'] + tokens + ['@']
    
    for i in range(0, len(tokens) - 3):
        countWord(tokens[i].lower() + ',' + 
                  tokens[i+1].lower() + ',' +
                  tokens[i+2].lower() + ',' + 
                  tokens[i+3].lower(), 
            occurrences, weight)
    
    return len(tokens) - 3

def countPentagrams(tokens, occurrences, weight=1):
    if len(tokens) <= 1:
        return 0

    tokens = ['@'] + tokens + ['@']
    
    for i in range(0, len(tokens) - 4):
        countWord(tokens[i].lower() + ',' + 
                  tokens[i+1].lower() + ',' +
                  tokens[i+2].lower() + ',' + 
                  tokens[i+3].lower() + ',' + 
                  tokens[i+4].lower(), 
            occurrences, weight)
    
    return len(tokens) - 4

def countHexagrams(tokens, occurrences, weight=1):
    if len(tokens) <= 2:
        return 0

    tokens = ['@'] + tokens + ['@']
    
    for i in range(0, len(tokens) - 5):
        countWord(tokens[i].lower() + ',' + 
                  tokens[i+1].lower() + ',' +
                  tokens[i+2].lower() + ',' + 
                  tokens[i+3].lower() + ',' + 
                  tokens[i+4].lower() + ',' + 
                  tokens[i+5].lower(), 
            occurrences, weight)
    
    return len(tokens) - 5

def countWord(word, occurrences, weight = 1):
    if word in occurrences:
        occurrences[word] += weight
    else:
        occurrences[word] = weight

def countNGrams(tokens, mode):
    W1, W2, W3 = (2, 1.15, 2) if mode == "-coarse" else (1.5, 1, 1.75)

    wordCount = {}
    countOccurrences(tokens, wordCount, W1)
    #countOccurrences(tokens, wordCount)
    countBigrams(tokens, wordCount, W2)
    #countTrigrams(tokens, wordCount)
    #countDistantBigrams(tokens, wordCount)
    #countQuadrigrams(tokens, wordCount)
    #countPentagrams(tokens, wordCount)
    #countHexagrams(tokens, wordCount)
    countStart(tokens, wordCount, W3)
    #countStart(tokens, wordCount)
    #countStart(tokens, wordCount)

    return wordCount