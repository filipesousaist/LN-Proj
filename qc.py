from sys import argv
from utils import cosine_similarity, sum2
import numpy as np
import re
import nltk

option, trainFilename, questionsFilename = argv[1:4]

# Coarse

CATEGORIES = [
    "ABBR",
    "DESC",
    "ENTY",
    "HUM",
    "LOC",
    "NUM"
]
NUM_CATS = len(CATEGORIES)

DELETE_CHARS = "\n!,;:"

STUPIDITY_COEFFICIENT = 290

ALL_UPPER = 1

STOP_WORDS_FILE = open("STOP_WORDS.txt", "r")
STOP_WORDS = STOP_WORDS_FILE.readlines()
for i in range(len(STOP_WORDS)):
    STOP_WORDS[i] = STOP_WORDS[i].rstrip('\n')
STOP_WORDS_FILE.close()

REGEXES = [re.compile(re.escape(word), re.IGNORECASE) for word in STOP_WORDS]

def getCategoriesAndQuestions(lines):
    categories = []
    questions = []
    for line in lines:
        tokens = line.split(" ")
        categories.append(tokens[0])
        questions.append(" ".join(tokens[1:]))
    
    return (categories, questions)

def removeSuffixes(question):
    tokens = nltk.word_tokenize(question)
    for i in range(len(tokens)):
        if tokens[i].endswith("ed"):
            tokens[i] = tokens[i][:-2]
    return " ".join(tokens)

def preProccess():
    trainFile = open(trainFilename, "r")
    lines = trainFile.readlines()
    trainFile.close()

    categories, questions = getCategoriesAndQuestions(lines)

    newQuestions = []
    #newQuestions = questions

    for q in questions:
        for char in DELETE_CHARS:
            q = q.replace(char, '')
        
        # Hall of fame:
        #q = removeSuffixes(q)
        """
        newQuestions.append(q.upper())
        """
        """
        tokens = q.split(" ")

        for i in range(1, len(tokens)):
            if tokens[i] and tokens[i][-1] == 's':
                tokens[i] = tokens[i].rstrip('s')
            
        newQuestions.append(" ".join(tokens))
        """

        lower = q.lower()
        for i in range(len(STOP_WORDS)):
            if STOP_WORDS[i] in lower:
                q = REGEXES[i].sub('', q)

        newQuestions.append(q)

    return (categories, newQuestions)

# debug
def findProblematicWords(wordCount):
    wordCats = {}
    for word in getAllWords(wordCount):
        wordCats[word] = []
        for cat in CATEGORIES:
            if word in wordCount[cat]:
                wordCats[word].append(wordCount[cat][word])
            else:
                wordCats[word].append(0)
        wordCats[word] = list(map(lambda c: c // 4, filter(lambda c: c >= 5, wordCats[word])))
        if len(wordCats[word]) - len(set(wordCats[word])) >= 2:
            print(word)
            input()

def calculateFrequencies(categories, questions):
    wordCount = {cat: {} for cat in CATEGORIES}
    totalCount = {cat: 0 for cat in CATEGORIES}

    for i in range(len(questions)):
        cat = categories[i].split(":")[0]
        tokens = nltk.word_tokenize(questions[i])
        
        totalCount[cat] += countOccurrences(tokens, wordCount[cat])
    
    #findProblematicWords(wordCount)

    for cat in CATEGORIES:

        #print(cat, ["%s: %d" % (w, wordCount[cat][w]) for w in wordCount[cat] if wordCount[cat][w] > 25])
        #input()

        for word in list(wordCount[cat].keys()):
            if wordCount[cat][word] == 1:
                wordCount[cat][word] = STUPIDITY_COEFFICIENT
                totalCount[cat] += STUPIDITY_COEFFICIENT - 1

        for word in wordCount[cat]:
            wordCount[cat][word] /= totalCount[cat]
    
    #print(wordCount)
    return wordCount

def countOccurrences(tokens, occurrences):
    length = len(tokens)
    for word in tokens:
        if word in occurrences:
            occurrences[word] += 1
        else:
            occurrences[word] = 1
        if word.isupper():
            length += 1
            if ALL_UPPER in occurrences:
                occurrences[ALL_UPPER] += 1
            else:
                occurrences[ALL_UPPER] = 1


    return length


def getAllWords(wordDicts):
    wordSet = set()

    for cat in CATEGORIES:
        for word in wordDicts[cat]:
            wordSet.add(word)
    return wordSet

def calculateSimilarities(wordCount):
    questionsFile = open(questionsFilename, "r")
    sentences = questionsFile.readlines()
    questionsFile.close()

    wordSet = getAllWords(wordCount)

    for s in sentences:
        #s = removeSuffixes(s)
        s_wordCount = {} 
        tokens = nltk.word_tokenize(s)

        countOccurrences(tokens, s_wordCount)

        s_wordFreq = {word : s_wordCount[word] for word in s_wordCount if word in wordSet}

        length = len(s_wordFreq)
        for word in s_wordFreq:
            s_wordFreq[word] /= length
        
        sims = np.zeros(NUM_CATS)
        for i in range(NUM_CATS):
            sims[i] = cosine_similarity(s_wordFreq, wordCount[CATEGORIES[i]])
        
        print(CATEGORIES[np.argmax(sims)])

calculateSimilarities(calculateFrequencies(*preProccess()))
