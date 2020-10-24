from const import ALL_UPPER

def countOccurrences(tokens, occurrences):
    length = len(tokens)
    for word in tokens:
        countWord(word, occurrences)
        if word.isupper():
            length += 1
            countWord(ALL_UPPER, occurrences)
    return length

def countStart(tokens, occurrences, n=1):
    for _ in range(n):
        countWord('@,' + tokens[0], occurrences)
    return n

def countBigrams(tokens, occurrences):
    tokens = ['@'] + tokens + ['@']
    
    for i in range(0, len(tokens) - 1):
        countWord(tokens[i].lower() + ',' + tokens[i+1].lower(), occurrences)
    
    return len(tokens) - 1

def countTrigrams(tokens, occurrences):
    tokens = ['@'] + tokens + ['@']
    
    for i in range(0, len(tokens) - 2):
        countWord(tokens[i].lower() + ',' + 
                  tokens[i+1].lower() + ',' + 
                  tokens[i+2].lower(), 
            occurrences)
    
    return len(tokens) - 2

def countQuadrigrams(tokens, occurrences):
    if len(tokens) == 0:
        return 0

    tokens = ['@'] + tokens + ['@']
    
    for i in range(0, len(tokens) - 3):
        countWord(tokens[i].lower() + ',' + 
                  tokens[i+1].lower() + ',' +
                  tokens[i+2].lower() + ',' + 
                  tokens[i+3].lower(), 
            occurrences)
    
    return len(tokens) - 3

def countPentagrams(tokens, occurrences):
    if len(tokens) <= 1:
        return 0

    tokens = ['@'] + tokens + ['@']
    
    for i in range(0, len(tokens) - 4):
        countWord(tokens[i].lower() + ',' + 
                  tokens[i+1].lower() + ',' +
                  tokens[i+2].lower() + ',' + 
                  tokens[i+3].lower() + ',' + 
                  tokens[i+4].lower(), 
            occurrences)
    
    return len(tokens) - 4

def countHexagrams(tokens, occurrences):
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
            occurrences)
    
    return len(tokens) - 5

def countWord(word, occurrences):
    if word in occurrences:
        occurrences[word] += 1
    else:
        occurrences[word] = 1

def countNGrams(tokens):
    wordCount = {}

    countOccurrences(tokens, wordCount)
    #countOccurrences(tokens, wordCount)
    countBigrams(tokens, wordCount)
    #countBigrams(tokens, wordCount)
    #countTrigrams(tokens, wordCount)
    #countQuadrigrams(tokens, wordCount)
    #countPentagrams(tokens, wordCount)
    #countHexagrams(tokens, wordCount)
    #countStart(tokens, wordCount)

    return wordCount