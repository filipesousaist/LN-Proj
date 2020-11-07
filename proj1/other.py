import nltk
import re
from const import COARSE_CATEGORIES, FINE_CATEGORIES

def getLabelsAndQuestions(lines):
    labels = []
    questions = []
    for line in lines:
        tokens = line.split(" ")
        labels.append(tokens[0])
        questions.append(" ".join(tokens[1:]))
    
    return (labels, questions)

def getAllWords(wordDicts):
    wordSet = set()
    for word in wordDicts:
        wordSet.add(word)
    return wordSet

def removeSuffixes(question, mode):
    tokens = nltk.word_tokenize(question)
    for i in range(len(tokens)):
        tk = tokens[i]
        l = len(tk)
        if l >= 4 and tk.endswith("ed"):
            if tk.endswith("sed"):
                tokens[i] = tk[:-1]
            else:
                tokens[i] = tk[:-2]
        elif mode == "-coarse" and l >= 5 and (
            tk.endswith("ing") or 
            tk.endswith("ity") or
            tk.endswith("ism") or 
            tk.endswith("ant") or 
            tk.endswith("age") or 
            tk.endswith("ery") ):
            tokens[i] = tk[:-3]
        #elif l >= 7 and (
            #tk.endswith("tion") or 
            #tk.endswith("ness") or 
            #tk.endswith("ment") or 
         #   tk.endswith("ship")):
         #   tokens[i] = tk[:-4]
        
        elif l >= 3 and tk.endswith("s") and not tk.endswith("ss"):
            tokens[i] = tk[:-1]

        #-tion, -ity, -er, -ness, -ism, -ment, -ant, -ship, -age, -ery
    return " ".join(tokens)


DELETE_CHARS = ":?.;!,@"

#STOP_WORDS_FILE = open("STOP_WORDS.txt", "r")
#STOP_WORDS = STOP_WORDS_FILE.readlines()
#for i in range(len(STOP_WORDS)):
#    STOP_WORDS[i] = STOP_WORDS[i].rstrip('\n')
#STOP_WORDS_FILE.close()

#REGEXES = [re.compile(re.escape(word), re.IGNORECASE) for word in STOP_WORDS]


def processSentence(s, mode):
    # Remove special characters
    for char in DELETE_CHARS:
        s = s.replace(char, '')
    
    # Remove suffixes
    s = removeSuffixes(s, mode)
    """
    # Remove stop words
    lower = s.lower()
    for i in range(len(STOP_WORDS)):
        if STOP_WORDS[i] in lower:
            s = REGEXES[i].sub('', s)
    """
    
    return s