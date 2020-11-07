from const import ALL_UPPER

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

def countTrigrams(tokens, occurrences, weight=1):
    tokens = ['@'] + tokens
    
    for i in range(0, len(tokens) - 2):
        countWord(tokens[i].lower() + ',' + 
                  tokens[i+1].lower() + ',' + 
                  tokens[i+2].lower(),
            occurrences, weight)

def countWord(word, occurrences, weight = 1):
    if word in occurrences:
        occurrences[word] += weight
    else:
        occurrences[word] = weight

def countNGrams(tokens, mode):
    W1, W2, WS = (2, 1.15, 2) if mode == "-coarse" else (1.5, 1, 1.75)

    wordCount = {}
    countOccurrences(tokens, wordCount, W1)
    countBigrams(tokens, wordCount, W2)
    countTrigrams(tokens, wordCount, 0.22)
    countStart(tokens, wordCount, WS)

    return wordCount