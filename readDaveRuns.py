import os
import copy
from runTimeEntry import runTimeEntry

def getRunTimeEntries():
    # note that path assumes script is being run from 505p1 subfolder
    # subfolder must be of depth 1 in 505p1
    # example script: 505p1/analysisFolder/exampleScript.py
    directory = "./../output/OfficialRuns/"

    runTimeEntries = []

    for subdir, dirs, files in os.walk(directory):
        for fileName in files:
            path = directory + fileName
            f = open(path, "r")
            fileReadFinished = False
            while not fileReadFinished:
                line = f.readline()
                # somewhat arbitrary test to make sure we haven't reached the end of file
                # unfortunately, the output files are structured a tad differently, and this works for all
                if len(line) > 5:
                    nextRunTimeEntry = runTimeEntry(line)
                    runTimeEntries.append(nextRunTimeEntry)
                else:
                    fileReadFinished = True
            f.close()

    # set the run number (so that we can eliminate outliers)
    # will be 1-13 where 1-3 is a warm-up
    runNumbers = {}
    for entry in runTimeEntries:
        # get the dict for the sort type
        sortType = entry.sortType
        if not sortType in runNumbers.keys():
            runNumbers[sortType] = {}
        sortTypeDict =  runNumbers[sortType]
        # get the dict for the folder
        folder = entry.inputFolder
        if not folder in sortTypeDict.keys():
            sortTypeDict[folder] = {}
        folderDict = sortTypeDict[folder]
        # get the current run for the file
        inputFile = entry.inputFile
        if not inputFile in folderDict.keys():
            folderDict[inputFile] = 0
        folderDict[inputFile] += 1
        entry.runNumber = folderDict[inputFile]

    return runTimeEntries
