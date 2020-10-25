import nltk

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
        
        elif l >= 3 and tk.endswith("s") and not tk.endswith("ss"):
            tokens[i] = tk[:-1]

    return " ".join(tokens)


DELETE_CHARS = ":?.;!,@"

def processSentence(s, mode):
    # Remove special characters
    for char in DELETE_CHARS:
        s = s.replace(char, '')
    
    # Remove suffixes
    s = removeSuffixes(s, mode)

    return s