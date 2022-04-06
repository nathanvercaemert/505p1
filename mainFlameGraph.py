import sys
import os
import time
import copy
from logEntry import logEntry
from sorts import mergeSort, insertionSort, mergeSortExpensive, insertionSortExpensive

# get the input file name
logFileName = sys.argv[1]
logFileNamePrint = logFileName.split('/')
logFileNamePrint = logFileNamePrint[-2] + '/' + logFileNamePrint[-1]
logFileNamePrint = logFileNamePrint.split('.')[0]

# get the output file name and make the directory if necessary
outputFileName = sys.argv[2]
outputDirectorySplit = outputFileName.split('/')
outputDirectorySplit = outputDirectorySplit[:-1]
outputDirectory = ""
for directory in outputDirectorySplit:
    outputDirectory += directory + "/"
if not os.path.exists(outputDirectory):
    os.makedirs(outputDirectory)

# get which type of sort
sortType = sys.argv[3]

# read the file into memory
timePreRead = time.process_time()
logFile = open(logFileName, "rb")
ar = []
while True:
    line = logFile.readline()
    if not line:
        break
    nextEntry = logEntry(line)
    ar.append(nextEntry)
logFile.close()
timePostRead = time.process_time()

# get cheap or expensive comparison
cheapOrExpensive = sys.argv[4]

numRuns = int(sys.argv[5])

workingList = []
for i in range(numRuns):
    workingList = copy.deepcopy(ar)
    print('Go')
    # sort the data
    timePreSort = time.process_time()
    if cheapOrExpensive == "c":
        if sortType == "m":
            workingList = mergeSort(workingList)
        if sortType == "i":
            insertionSort(workingList)
        if sortType == "t":
            workingList.sort()
    else:
        if sortType == "m":
            workingList = mergeSortExpensive(workingList)
        if sortType == "i":
            insertionSortExpensive(workingList)
        if sortType == "t":
            workingList.sort()
    timePostSort = time.process_time()

    # check that data is sorted
    isSorted = all(workingList[i] <= workingList[i+1] for i in range(len(workingList) - 1))

    # write output file
    outputFile = open(outputFileName, "wb")
    for entry in workingList:
        toWrite = bytearray(entry.entry)
        outputFile.write(toWrite)

    printString = sortType + ","
    printString += cheapOrExpensive + ","
    printString += logFileNamePrint + ","
    printString += str(isSorted) + ","
    if i == 0:
        printString += str(timePostRead - timePreRead) + ","
    else:
        printString += str(0) + ","
    printString += str(timePostSort - timePreSort)
    print(printString)
