from other import getAllWords
from const import COARSE_CATEGORIES, FINE_CATEGORIES

def findProblematicWords(wordCount, mode):
    wordCats = {}
    cats = (COARSE_CATEGORIES if mode == '-coarse' else FINE_CATEGORIES)
    for word in getAllWords(wordCount):
        wordCats[word] = []
        for cat in cats:
            if word in wordCount[cat]:
                wordCats[word].append(wordCount[cat][word])
            else:
                wordCats[word].append(0)
        wordCats[word] = list(map(lambda c: c // 5, filter(lambda c: c >= 3, wordCats[word])))
        if len(wordCats[word]) - len(set(wordCats[word])) >= 3:
            print(word)
            input()