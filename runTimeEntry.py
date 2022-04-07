class runTimeEntry:
    def __init__(self, entry):
        # remove newline from end
        if entry[-1] == '\n':
            entry = entry[:-1]

        entry = entry.split(',')
        self.sortType = entry[0]
        self.cheapOrExpensive = entry[1]
        inputFileAndFolder = entry[2]
        inputFileAndFolder = inputFileAndFolder.split('/')
        self.inputFolder = inputFileAndFolder[0]
        self.inputFile = int(inputFileAndFolder[1])
        self.isSorted = entry[3]
        self.readTime = float(entry[4])
        self.sortTime = float(entry[5])
        self.runNumber = -1
