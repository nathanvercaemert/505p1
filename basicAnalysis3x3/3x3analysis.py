import sys
sys.path.append('..')
import matplotlib.pyplot as plt
import statistics
import math
from scipy.optimize import curve_fit
import numpy

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


def quadraticCurveFit(x, a, b, c):
    return a*x**2 + b*x + c


def nLogNCurveFit(x, a, b, c):
    return a*x + b*numpy.log2(x) + c


# def quadraticCurveFit(x, a, b):
#     return a*x**2 + b*x


# def nLogNCurveFit(x, a, b):
#     return a*x + b*numpy.log2(x)

# def makePositive(ar):
#     least = numpy.inf
#     for element in ar:
#         if element < least:
#             least = element
#     if least < 0:
#         for index, element in enumerate(ar):
#             ar[index] += least


# toPlot is list of tuples (x, y)
def plotFolderLogLogCurveFit(insertionToPlot, mergeToPlot, timToPlot, folder):
    plt.clf()
    iX = []
    iXlog = []
    iY = []
    iYlog = []
    for point in insertionToPlot:
        iX.append(point[0])
        iXlog.append(math.log(point[0], 2))
        iY.append(point[1])
        iYlog.append(math.log(point[1], 2))
    mX = []
    mXlog = []
    mY = []
    mYlog = []
    for point in mergeToPlot:
        mX.append(point[0])
        mXlog.append(math.log(point[0], 2))
        mY.append(point[1])
        mYlog.append(math.log(point[1], 2))
    tX = []
    tXlog = []
    tY = []
    tYlog = []
    for point in timToPlot:
        tX.append(point[0])
        tXlog.append(math.log(point[0], 2))
        tY.append(point[1])
        tYlog.append(math.log(point[1], 2))
    plt.plot(iX, iY, '-', label="i", color="mediumslateblue")
    # plt.plot(mXlog, mYlog, '-', label="m", color="darkorange")
    # plt.plot(tXlog, tYlog, '-', label="t", color="mediumslateblue")

    iXAr = numpy.array(iX)
    iYAr = numpy.array(iY)
    iOpt, iCov = curve_fit(quadraticCurveFit, iXAr, iYAr)
    # iOpt, iCov = curve_fit(quadraticCurveFit, iXAr, iYAr, bounds=([-numpy.inf, 0, -numpy.inf], numpy.inf))
    iYAr = quadraticCurveFit(iXAr, *iOpt)
    # iXArLog = numpy.log2(iXAr)
    # makePositive(iYAr)
    # iYArLog = []
    # for index, y in enumerate(iYAr):
    #     try:
    #         iYArLog.append(math.log(y, 2))
    #     except Exception as e:
    #         iYArLog.append(0)
    # iYArLog = numpy.log2(iYAr)
    plt.plot(iXAr, iYAr, '--', label='fit: a=%5.3f, b=%5.3f, c=%5.3f' % tuple(iOpt), color="darkorange")
    # plt.plot(iXArLog, iYArLog, '--', label='fit: a=%5.3f, b=%5.3f' % tuple(iOpt), color="darkturquoise")

    # mXAr = numpy.array(mX)
    # mYAr = numpy.array(mY)
    # mOpt, mCov = curve_fit(nLogNCurveFit, mXAr, mYAr)
    # # mOpt, mCov = curve_fit(nLogNCurveFit, mXAr, mYAr, bounds=([-numpy.inf, 0, -numpy.inf], numpy.inf))
    # mYAr = nLogNCurveFit(mXAr, *mOpt)
    # mXArLog = numpy.log2(mXAr)
    # mYArLog = numpy.log2(mYAr)
    # plt.plot(mXAr, mYAr, '--', label='fit: a=%5.3f, b=%5.3f, c=%5.3f' % tuple(mOpt), color="darkorange")
    # # plt.plot(mXArLog, mYArLog, '--', label='fit: a=%5.3f, b=%5.3f' % tuple(mOpt), color="darkorange")

    # tXAr = numpy.array(tX)
    # tYAr = numpy.array(tY)
    # tOpt, tCov = curve_fit(nLogNCurveFit, tXAr, tYAr)
    # # tOpt, tCov = curve_fit(nLogNCurveFit, tXAr, tYAr, bounds=([-numpy.inf, 0, -numpy.inf], numpy.inf))
    # tYAr = nLogNCurveFit(tXAr, *tOpt)
    # tXArLog = numpy.log2(tXAr)
    # tYArLog = numpy.log2(tYAr)
    # plt.plot(tXAr, tYAr, '--', label='fit: a=%5.3f, b=%5.3f, c=%5.3f' % tuple(tOpt), color="mediumslateblue")
    # # plt.plot(tXArLog, tYArLog, '--', label='fit: a=%5.3f, b=%5.3f' % tuple(tOpt), color="mediumslateblue")

    plt.legend()
    plt.show()


# plotFolderLogLog(insertionAToPlot, mergeAToPlot, timAToPlot, "A")
# plotFolderLogVsRaw(insertionAToPlot, mergeAToPlot, timAToPlot, "A")
# plotFolder(insertionAToPlot, mergeAToPlot, timAToPlot, "A")
plotFolderLogLogCurveFit(insertionAToPlot, mergeAToPlot, timAToPlot, "A")
