from sys import argv
from const import *
import time

devLabelsFilename, predictedLabelsFilename = argv[1:3]

devLabelsFile = open(devLabelsFilename, "r")
devLabels = devLabelsFile.readlines()
devLabelsFile.close()

predictedLabelsFile = open(predictedLabelsFilename, "r")
predictedLabels = predictedLabelsFile.readlines()
predictedLabelsFile.close()

def evaluate(cats, getCat):
    totalOK = 0
    catsOK = {cat: 0 for cat in cats}
    catsCount = {cat: 0 for cat in cats}

    for i in range(numLabels):
        realCat = getCat(devLabels[i])
        result = int(realCat == predictedLabels[i].rstrip('\n'))
        catsOK[realCat] += result
        totalOK += result
        catsCount[realCat] += 1

    for cat in cats:
        if catsCount[cat] > 0:
            print(cat.ljust(15) + ("%f%%" % ((catsOK[cat] / catsCount[cat]) * 100)).rjust(15))

    print("Total: \t%f%%" % ((totalOK / numLabels) * 100))

numLabels = len(devLabels)

if ':' in predictedLabels[0]:
    print("+------+")
    print("| FINE |")
    print("+------+")
    evaluate(FINE_CATEGORIES, lambda lbl: lbl.rstrip('\n'))
else:
    print("+--------+")
    print("| COARSE |")
    print("+--------+")
    evaluate(COARSE_CATEGORIES, lambda lbl: lbl.split(':')[0])
