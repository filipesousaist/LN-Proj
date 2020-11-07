from sys import argv
from count import countNGrams
from other import getLabelsAndQuestions, processSentence, getAllWords
import nltk

from sklearn.svm import LinearSVC
from sklearn.feature_extraction import DictVectorizer

mode, trainFilename, questionsFilename = argv[1:4]

def preProccess():
    trainFile = open(trainFilename, "r")
    lines = trainFile.readlines()
    trainFile.close()

    labels, questions = getLabelsAndQuestions(lines)

    newQuestions = [processSentence(q, mode) for q in questions]

    getLabel = \
        (lambda lbl: lbl.split(":")[0]) \
        if mode == '-coarse' else \
        (lambda lbl: lbl.rstrip("\n"))

    return (list(map(getLabel, labels)), newQuestions)


def calculateWordCounts(labels, questions):
    numQuestions = len(questions)

    totalWordCount = {}
    wordCount = []

    for i in range(numQuestions):
        tokens = nltk.word_tokenize(questions[i])

        currentWordCount = countNGrams(tokens, mode)
        wordCount.append(currentWordCount)
        for word in currentWordCount:
            if word in totalWordCount:
                totalWordCount[word] += 1
            else:
                totalWordCount[word] = 1
    
    return (labels, wordCount, getAllWords(totalWordCount))

def learn(labels, wordCount, knownWords): 
    X = DictVectorizer().fit_transform(wordCount)
    clf = LinearSVC(random_state=0, tol=1e-2, max_iter=100000)
    clf.fit(X, labels)

    return (clf, knownWords)

def predict(clf, knownWords):
    questionsFile = open(questionsFilename, "r")
    questions = questionsFile.readlines()
    questionsFile.close()

    # Count N-grams for each question in the test set
    testWordCount = []

    for q in questions:
        q = processSentence(q, mode)
        tokens = nltk.word_tokenize(q)

        wordCount = countNGrams(tokens, mode)
        newWordCount = {}
        for word in wordCount:
            if word in knownWords:
                newWordCount[word] = wordCount[word]
        testWordCount.append(newWordCount)
    
    # Add missing features as "dummies" to the test set
    for word in knownWords:
        if word not in testWordCount[0]:
            testWordCount[0][word] = 0

    # Test
    testX = DictVectorizer().fit_transform(testWordCount)
    for lbl in clf.predict(testX):
        print(lbl)

predict(*learn(*calculateWordCounts(*preProccess())))
