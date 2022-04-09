import os
from unicodedata import name
import pandas as pd
import matplotlib.pyplot as plt

from sympy import true

# folder relative to current location
directory = "./output_copy/OfficialRuns_copy/"
# should find all files in the directory folder
file_list = os.listdir(directory)

df = pd.DataFrame()

# append all files into 1 dataframe
for file in file_list:
    data = pd.read_csv(directory + file)
    df = pd.concat([df, pd.DataFrame(data)], ignore_index=True)


# turn the column files into folder and size and split
df[['folder', 'size']] = df['file'].str.split('/', expand=True)
# drop the unneeded column file
df = df.drop(columns='file')

# possible options
costs = ['c', 'e']
sortTypes = ['i', 'm', 't']
folders = ['A', 'B', 'C']

# confirmed all sorted
# print(df.loc[df['sorted'] == False])
df = df.drop(columns='sorted')

# don't really need preprocess time
df = df.drop(columns='preProcessTime')

dfs = pd.DataFrame()#(columns = ['sortType', 'cost', 'folder', 'sizeList', 'timeList'])
#print(dfs)

# https://localcoder.org/pandas-group-by-remove-outliers
def is_outlier(s):
    # https://towardsdatascience.com/practical-implementation-of-outlier-detection-in-python-90680453b3ce
    Q1 = s['sortTime'].quantile(.25)
    Q3 = s['sortTime'].quantile(.75)
    IQR = Q3 - Q1
    return s.loc[~((s['sortTime'] < (Q1 - 1.5 * IQR)) | (s['sortTime'] > (Q3 + 1.5 * IQR)))]

# every combination individually
for cost in costs:
    for sortType in sortTypes:
        for folder in folders:
            dfNew = df.loc[(df['sortType'] == sortType) & (df['cost'] == cost) & (df['folder'] == folder)]
            
            # group by equivalent size, drop the warmup items
            dfNew = dfNew.groupby('size').apply(lambda x: x.iloc[3:] if len(x) == 13 else x.iloc[2:]).reset_index(drop=True)
            dfNew = dfNew.groupby('size').apply(is_outlier).reset_index(drop=True)
            #pd.set_option("display.max_rows", None, "display.max_columns", None)
            #print(dfNew) 
            # group again by size
            
            dfNew = dfNew.groupby('size')['sortTime'].mean()
            # convert index to int and sort
            dfNew.index = dfNew.index.astype(int)
            dfNew = dfNew.sort_index()
            print(dfNew)
            
            #pd.set_option("display.max_rows", None, "display.max_columns", None)
            #plt.plot(dfNew.index.tolist(), dfNew.tolist())
            #plt.title(cost + sortType + folder)
            #plt.xlabel("size")
            #plt.ylabel("time")
            #plt.show()
            dfs = pd.concat([dfs, pd.DataFrame([{'sortType':sortType, 'cost':cost, 'folder':folder, 'sizeList':dfNew.index.tolist(), 'timeList':dfNew.tolist()}])], ignore_index=True)
            
print(dfs)