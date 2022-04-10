import os
from logEntry import logEntry

directory = f'./../../csc505-spring-2022/Project1/C'
files = os.listdir(directory)

for file in files:
    with open(directory + '/' + file, 'r') as f:
        #lines = f.readlines()
        ar = []
        while True:
            line = f.readline()
            if not line:
                break
            nextEntry = logEntry(line)
            ar.append(nextEntry)
        
        print(file + all(ar[i] <= ar[i+1] for i in range(len(ar) - 1)))