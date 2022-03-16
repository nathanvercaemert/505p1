import sys
import copy
from logEntry import logEntry
from sorts import mergeSort, insertionSort

logFile = open(sys.argv[1], "r")

ar = []
while True:
    line = logFile.readline()
    if not line:
        break
    nextEntry = logEntry(line)
    ar.append(nextEntry)

mergeAr = copy.copy(ar)
insertionAr = copy.copy(ar)
timAr = copy.copy(ar)

mergeAr = mergeSort(mergeAr)
insertionSort(insertionAr)
timAr.sort

mergeOut = open("./test/mergeSortTest/output.log", "w")
for entry in mergeAr:
    mergeOut.write(entry.entry)
insertionOut = open("./test/insertionSortTest/output.log", "w")
for entry in insertionAr:
    insertionOut.write(entry.entry)
timOut = open("./test/timsortTest/output.log", "w")
for entry in timAr:
    timOut.write(entry.entry)
