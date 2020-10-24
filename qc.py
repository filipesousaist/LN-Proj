from sys import argv
from utils import *
from const import *
from count import *
from other import getLabelsAndQuestions, processSentence, getAllWords
from debug import findProblematicWords
import numpy as np
import re
import nltk

from sklearn.svm import LinearSVC
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_classification
from sklearn.feature_extraction import DictVectorizer

mode, trainFilename, questionsFilename = argv[1:4]

def preProccess():
    trainFile = open(trainFilename, "r")
    lines = trainFile.readlines()
    trainFile.close()

    labels, questions = getLabelsAndQuestions(lines)

    newQuestions = [processSentence(q) for q in questions]

    getLabel = \
        (lambda lbl: lbl.split(":")[0]) \
        if mode == '-coarse' else \
        (lambda lbl: lbl.rstrip("\n"))

    newLabels = list(map(getLabel, labels))

    return (newLabels, newQuestions)


def calculateWordCounts(labels, questions):
    numQuestions = len(questions)

    totalWordCount = {}
    wordCount = []

    for i in range(numQuestions):
        s = processSentence(questions[i])
        tokens = nltk.word_tokenize(s)

        currentWordCount = countNGrams(tokens)
        wordCount.append(currentWordCount)
        for word in currentWordCount:
            if word in totalWordCount:
                totalWordCount[word] += 1
            else:
                totalWordCount[word] = 1
    """
    toKeep = set()
    for word in totalWordCount:
        if totalWordCount[word] > 1:
            toKeep.add(word)
    for i in range(len(wordCount)):
        newCount = {}
        for word in wordCount[i]:
            if word in toKeep:
                newCount[word] = wordCount[i][word]
        wordCount[i] = newCount
    """

    #findProblematicWords(wordCount, mode)
        
    #print(wordCount)
    
    return (labels, wordCount, getAllWords(totalWordCount))

def learn(labels, wordCount, toKeep):
    dv = DictVectorizer() 
    X = dv.fit_transform(wordCount)
    clf = LinearSVC(random_state=1, tol=0.01, max_iter=100000, verbose=False)
    clf.fit(X, labels)

    return (clf, toKeep, dv)
#Pipeline(steps=[('standardscaler', StandardScaler()),
#                ('linearsvc', LinearSVC(random_state=0, tol=1e-05))])


def predict(clf, toKeep, dv):
    questionsFile = open(questionsFilename, "r")
    sentences = questionsFile.readlines()
    questionsFile.close()

    testWordCount = []

    for s in sentences:
        s = processSentence(s)
        tokens = nltk.word_tokenize(s)

        wordCount = countNGrams(tokens)
        newWordCount = {}
        for word in wordCount:
            if word in toKeep:
                newWordCount[word] = wordCount[word]
        testWordCount.append(newWordCount)
    
    for word in toKeep:
        if word not in testWordCount[0]:
            testWordCount[0][word] = 0

    testX = dv.fit_transform(testWordCount)

    for lbl in clf.predict(testX):
        print(lbl)

predict(*learn(*calculateWordCounts(*preProccess())))
