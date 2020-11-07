import math

def cosine_similarity(v1, v2):
    # |v1.v2| / (|v1||v2|)
    
    return dot_product(v1, v2) / (sum2(v1) * sum2(v2)) ** (1/2)

def sum2(v):
    total = 0
    for w in v:
        total += v[w]**2
    return total if total > 0 else 1

def dot_product(v1, v2):
    total = 0
    for w in set(list(v1.keys()) + list(v2.keys())):
        if w in v1 and w in v2:
            total += v1[w] * v2[w]
    return total

def tfidf(w, cat, cats, wordCount, totalCount):
    return tf(w, cat, wordCount, totalCount) * idf(w, cats, wordCount)

def tf(w, cat, wordCount, totalCount):
    return (wordCount[cat][w] if w in wordCount[cat] else 0) / totalCount[cat]

def idf(w, cats, wordCount):
    catsCount = len([1 for cat in cats if w in wordCount[cat]])
    return math.log(len(cats) / catsCount) if catsCount > 0 else 0
