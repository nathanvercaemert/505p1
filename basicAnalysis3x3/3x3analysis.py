import sys
sys.path.append('..')
import matplotlib.pyplot as plt
import statistics
import math

from readDaveRuns import getRunTimeEntries

runTimeEntries = getRunTimeEntries()

insertionAEntries = []
insertionBEntries = []
insertionCEntries = []
mergeAEntries = []
mergeBEntries = []
mergeCEntries = []
timAEntries = []
timBEntries = []
timCEntries = []

for entry in runTimeEntries:
    if entry.sortType == "i":
        if entry.inputFolder == "A":
            insertionAEntries.append(entry)
        elif entry.inputFolder == "B":
            insertionBEntries.append(entry)
        else:
            insertionCEntries.append(entry)
    elif entry.sortType == "m":
        if entry.inputFolder == "A":
            mergeAEntries.append(entry)
        elif entry.inputFolder == "B":
            mergeBEntries.append(entry)
        else:
            mergeCEntries.append(entry)
    else:
        if entry.inputFolder == "A":
            timAEntries.append(entry)
        elif entry.inputFolder == "B":
            timBEntries.append(entry)
        else:
            timCEntries.append(entry)


def removeOutliers(actualRuns):
    return actualRuns


# runs is list of tuples where each tuple is (runNumber, sortTime)
def runTimeToPlot(runs):
    numRuns = len(runs)
    actualRuns = []
    if numRuns == 13:
        for run in runs:
            if run[0] > 3:
                actualRuns.append(run[1])
    # elif numRuns == 5:
    else:
        for run in runs:
            actualRuns.append(run[1])
    actualRuns = removeOutliers(actualRuns)
    return statistics.mean(actualRuns)


def getPlotPoints(entries):
    plotPoints = []
    inputFilesAllRuns = {}
    for entry in entries:
        inputFile = entry.inputFile
        if not inputFile in inputFilesAllRuns.keys():
            inputFilesAllRuns[inputFile] = []
        inputFilesAllRuns[inputFile].append((entry.runNumber, entry.sortTime))
    inputFilesProcessedRuns = {}
    for index, (inputFile, runs) in enumerate(inputFilesAllRuns.items()):
        if not inputFile in inputFilesProcessedRuns.keys():
            inputFilesProcessedRuns[inputFile] = []
        toPlot = runTimeToPlot(runs)
        inputFilesProcessedRuns[inputFile] = toPlot
    sortedInputFiles = []
    for key in inputFilesProcessedRuns.keys():
        sortedInputFiles.append(key)
    sortedInputFiles.sort()
    pointsToPlot = []
    for inputFile in sortedInputFiles:
        pointsToPlot.append((inputFile, inputFilesProcessedRuns[inputFile]))
    return pointsToPlot


# lists of tuples
# each tuple is (number of log entries, sort time)
insertionAToPlot = getPlotPoints(insertionAEntries)
insertionBToPlot = getPlotPoints(insertionBEntries)
insertionCToPlot = getPlotPoints(insertionCEntries)
mergeAToPlot = getPlotPoints(mergeAEntries)
mergeBToPlot = getPlotPoints(mergeBEntries)
mergeCToPlot = getPlotPoints(mergeCEntries)
timAToPlot = getPlotPoints(timAEntries)
timBToPlot = getPlotPoints(timBEntries)
timCToPlot = getPlotPoints(timCEntries)


# toPlot is list of tuples (x, y)
def plotFolderLogLog(insertionToPlot, mergeToPlot, timToPlot, folder):
    plt.clf()
    ilog = []
    for point in insertionToPlot:
        ilog.append(math.log(point[1], 2))
    mlog = []
    for point in mergeToPlot:
        mlog.append(math.log(point[1], 2))
    tlog = []
    for point in timToPlot:
        tlog.append(math.log(point[1], 2))
    plt.plot(ilog, label="i")
    plt.plot(mlog, label="m")
    plt.plot(tlog, label="t")
    plt.legend()
    plt.show()


# toPlot is list of tuples (x, y)
def plotFolderLogVsRaw(insertionToPlot, mergeToPlot, timToPlot, folder):
    plt.clf()
    iSortTime = []
    for point in insertionToPlot:
        iSortTime.append(point[1])
    mSortTime = []
    for point in mergeToPlot:
        mSortTime.append(point[1])
    tSortTime = []
    for point in timToPlot:
        tSortTime.append(point[1])
    plt.plot(iSortTime, label="i")
    plt.plot(mSortTime, label="m")
    plt.plot(tSortTime, label="t")
    plt.legend()
    plt.show()


# toPlot is list of tuples (x, y)
def plotFolder(insertionToPlot, mergeToPlot, timToPlot, folder):
    plt.clf()
    iX = []
    iY = []
    for point in insertionToPlot:
        iX.append(point[0])
        iY.append(point[1])
    mX = []
    mY = []
    for point in mergeToPlot:
        mX.append(point[0])
        mY.append(point[1])
    tX = []
    tY = []
    for point in timToPlot:
        tX.append(point[0])
        tY.append(point[1])
    plt.plot(iX, iY, label="i")
    plt.plot(mX, mY, label="m")
    plt.plot(tX, tY, label="t")
    plt.legend()
    plt.show()


plotFolderLogLog(insertionAToPlot, mergeAToPlot, timAToPlot, "A")
# plotFolderLogVsRaw(insertionAToPlot, mergeAToPlot, timAToPlot, "A")
# plotFolder(insertionAToPlot, mergeAToPlot, timAToPlot, "A")
