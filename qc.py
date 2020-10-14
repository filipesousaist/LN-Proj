from sys import argv

option, trainFilename, questionsFilename = argv[1:4]


trainFile = open(trainFilename, "r")

# Coarse

CATEGORIES = [
    "ABBR",
    "DESC",
    "ENTY",
    "HUM",
    "LOC",
    "NUM"
]

wordCount = {}
for cat in CATEGORIES:
    wordCount[cat] = {}

line = trainFile.readline()
while line:
    tokens = line.split(" ")

    cat = tokens[0].split(":")[0]

    line = trainFile.readline()

    for word in tokens[1:]:
        if word in wordCount[cat]:
            wordCount[cat][word] += 1
        else:
            wordCount[cat][word] = 1


print(list(wordCount["LOC"]))
