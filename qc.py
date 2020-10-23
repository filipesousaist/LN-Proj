from sys import argv
from utils import *
from const import *
from count import *
from other import getCategoriesAndQuestions, processSentence
from debug import findProblematicWords
import numpy as np
import re
import nltk

option, trainFilename, questionsFilename = argv[1:4]

def preProccess(mode):
    trainFile = open(trainFilename, "r")
    lines = trainFile.readlines()
    trainFile.close()

    categories, questions = getCategoriesAndQuestions(lines)

    newQuestions = [processSentence(q) for q in questions]

    return (categories, newQuestions, mode)


def calculateFrequencies(categories, questions, mode):
    cats = COARSE_CATEGORIES if mode == '-coarse' else FINE_CATEGORIES
    wordCount = {cat: {} for cat in cats}
    totalCount = {cat: 0 for cat in cats}

    for i in range(len(questions)):
        cat = categories[i].split(":")[0] if mode == '-coarse' else categories[i].rstrip('\n')
        tokens = nltk.word_tokenize(questions[i])

        totalCount[cat] += countNGrams(tokens, wordCount[cat])
    
    #findProblematicWords(wordCount, mode)
        
    #print(wordCount)
    
    return (wordCount, totalCount, mode)


def calculateSimilarities(wordCount, totalCount, mode):
    questionsFile = open(questionsFilename, "r")
    sentences = questionsFile.readlines()
    questionsFile.close()

    for s in sentences:
        s = processSentence(s)
        sWordCount = {} 
        tokens = nltk.word_tokenize(s)

        countNGrams(tokens, sWordCount)
        
        cats, numCats = \
            (COARSE_CATEGORIES, NUM_COARSE_CATS) \
            if mode == '-coarse' else \
            (FINE_CATEGORIES, NUM_FINE_CATS)

        sims = np.zeros(numCats)
        for i in range(numCats):
            for w in sWordCount:  
                sims[i] += tfidf(w, cats[i], cats, wordCount, totalCount) * sWordCount[w]
        
        print(cats[np.argmax(sims)])

calculateSimilarities(*calculateFrequencies(*preProccess(option)))
