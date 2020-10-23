import nltk
import re
from const import COARSE_CATEGORIES, FINE_CATEGORIES

def getCategoriesAndQuestions(lines):
    categories = []
    questions = []
    for line in lines:
        tokens = line.split(" ")
        categories.append(tokens[0])
        questions.append(" ".join(tokens[1:]))
    
    return (categories, questions)

def getAllWords(wordDicts, mode):
    wordSet = set()

    for cat in (COARSE_CATEGORIES if mode == '-coarse' else FINE_CATEGORIES):
        for word in wordDicts[cat]:
            wordSet.add(word)
    return wordSet

def removeSuffixes(question):
    tokens = nltk.word_tokenize(question)
    for i in range(len(tokens)):
        if tokens[i].endswith("ed"):
            tokens[i] = tokens[i][:-2]
        elif tokens[i].endswith("ing"):
            tokens[i] = tokens[i][:-3]
        elif len(tokens[i]) >= 3 and tokens[i].endswith("s") and not tokens[i].endswith("ss"):
            tokens[i] = tokens[i][:-1]
    return " ".join(tokens)


DELETE_CHARS = ":;!,@"

STOP_WORDS_FILE = open("STOP_WORDS.txt", "r")
STOP_WORDS = STOP_WORDS_FILE.readlines()
for i in range(len(STOP_WORDS)):
    STOP_WORDS[i] = STOP_WORDS[i].rstrip('\n')
STOP_WORDS_FILE.close()

REGEXES = [re.compile(re.escape(word), re.IGNORECASE) for word in STOP_WORDS]

def processSentence(s):
    # Remove special characters
    for char in DELETE_CHARS:
        s = s.replace(char, '')
    
    # Remove suffixes
    s = removeSuffixes(s)

    # Remove stop words
    lower = s.lower()
    for i in range(len(STOP_WORDS)):
        if STOP_WORDS[i] in lower:
            s = REGEXES[i].sub('', s)
    
    return s