from sys import argv

devLabelsFilename, predictedLabelsFilename = argv[1:3]

devLabelsFile = open(devLabelsFilename, "r")
devLabels = devLabelsFile.readlines()
devLabelsFile.close()

predictedLabelsFile = open(predictedLabelsFilename, "r")
predictedLabels = predictedLabelsFile.readlines()
predictedLabelsFile.close()

numLabels = len(devLabels)
coarseOK = 0

for i in range(numLabels):
    coarseOK += int(devLabels[i].split(":")[0] == predictedLabels[i].rstrip('\n'))

print("%f" % ((coarseOK / numLabels) * 100))

