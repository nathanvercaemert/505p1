import os
from logEntry import logEntry

directory = './csc505-spring-2022/Project1/C/'
files = os.listdir(directory)

files.sort(key=lambda x: int(os.path.splitext(x)[0]))
# print(files)
# exit()

# files.sort()

for file in files:
    # print(directory + file)
    # continue
    with open(directory + file, 'rb') as f:
        ar = []
        while True:
            line = f.readline()
            if not line:
                break
            nextEntry = logEntry(line)
            ar.append(nextEntry)

            extent = 0
            for i in range(len(ar) - 1):
                if ar[i] > ar[i+1]:
                    extent += 1
            extent /= len(ar)
        # print(str(file), str(all(ar[i] <= ar[i+1] for i in range(len(ar) - 1))), extent + "% unsorted")
        print(str(file), str(extent) + "% unsorted")
