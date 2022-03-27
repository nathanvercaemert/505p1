import sys
import os
import time
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

# sort the data
timePreSort = time.process_time()
if cheapOrExpensive == "c":
    if sortType == "m":
        ar = mergeSort(ar)
    if sortType == "i":
        insertionSort(ar)
    if sortType == "t":
        ar.sort()
else:
    if sortType == "m":
        ar = mergeSortExpensive(ar)
    if sortType == "i":
        insertionSortExpensive(ar)
    if sortType == "t":
        ar.sort()
timePostSort = time.process_time()

# check that data is sorted
isSorted = all(ar[i] <= ar[i+1] for i in range(len(ar) - 1))

# write output file
outputFile = open(outputFileName, "wb")
for entry in ar:
    toWrite = bytearray(entry.entry)
    outputFile.write(toWrite)

printString = sortType + ","
printString += cheapOrExpensive + ","
printString += logFileNamePrint + ","
printString += str(isSorted) + ","
printString += str(timePostRead - timePreRead) + ","
printString += str(timePostSort - timePreSort)
print(printString)
