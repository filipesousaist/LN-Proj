
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