from cProfile import label
import os
from unicodedata import name
from matplotlib import style
from numpy import dtype
import pandas as pd
import matplotlib.pyplot as plt
import math
from scipy.optimize import curve_fit
import scipy.optimize as opt
from scipy.optimize import curve_fit
import numpy as np
from scipy.interpolate import UnivariateSpline


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
# make size an int
df['size'] = df['size'].astype(int)
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

dfs = pd.DataFrame()
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
            # group again by size
            
            dfNew = dfNew.groupby('size')['sortTime'].mean()
            dfNew = dfNew.sort_index()

            dfs = pd.concat([dfs, pd.DataFrame([{'sortType':sortType, 'cost':cost, 'folder':folder, 'sizeList':dfNew.index.values, 'timeList':dfNew.values}])], ignore_index=True)

# full print
pd.set_option("display.max_rows", None, "display.max_columns", None)

def quadraticCurveFit(x, a, b, c):
    return a * x**2 + b * x + c

def nLogNCurveFit(x, a, b, c):
    return a * x + b * np.log2(x) + c

def displayPlot(folder, cost, sortTypeList, plotTitle, funcToApplySize, funcToApplyTime):
    plt.clf()
    p =  dfs.loc[(dfs['folder'] == folder) & (dfs['cost'] == cost)]
    p = p.explode(['sizeList', 'timeList'], ignore_index=True)
    p['sizeList'] = p['sizeList'].astype(int)
    p['timeList'] = p['timeList'].astype(float)
    p['sizeList'] = p['sizeList'].apply(funcToApplySize)
    p['timeList'] = p['timeList'].apply(funcToApplyTime)
    for sortType in sortTypeList:
        print(p.loc[p['sortType'] == sortType]['sizeList'])
        x = p.loc[p['sortType'] == sortType]['sizeList']
        y = p.loc[p['sortType'] == sortType]['timeList']

        s = UnivariateSpline(x, y, s=5)
        xs = np.linspace(0, 29, 100)
        ys = s(xs)

        plt.scatter(x, y, label=sortType)
        #plt.plot(x, y, 'o')
        #plt.plot(xs, ys)
        # # The actual curve fitting happens here
        optimizedParameters, _ = opt.curve_fit(nLogNCurveFit , x, y)

        # Use the optimized parameters to plot the best fit
        plt.plot(x, nLogNCurveFit(x, *optimizedParameters), label="fit")
    

    plt.xlabel('size')
    plt.ylabel('time')
    plt.ticklabel_format(style='plain')
    plt.legend()
    plt.title(plotTitle)
  # plt.savefig(outputfile)
    plt.show()

def dummyFunction(s):
    return s

def logFunction(s):
    return math.log(s + 1)

#Cheap plots for each folder 9 plots
#displayPlot('A', 'c', ['i'], 'Insertion Sort Folder A Cheap', dummyFunction,dummyFunction)
#displayPlot('B', 'c', ['i'], 'Insertion Sort Folder B Cheap', dummyFunction,dummyFunction)
displayPlot('C', 'c', ['i'], 'Insertion Sort Folder C Cheap', logFunction,logFunction)
#displayPlot('A', 'c', ['m'], 'Merge Sort Folder A Cheap', dummyFunction,dummyFunction)
#displayPlot('B', 'c', ['m'], 'Merge Sort Folder B Cheap', logFunction,logFunction)
#displayPlot('C', 'c', ['m'], 'Merge Sort Folder C Cheap', dummyFunction,dummyFunction)
#displayPlot('A', 'c', ['t'], 'Tim Sort Folder A Cheap', dummyFunction,dummyFunction)
#displayPlot('B', 'c', ['t'], 'Tim Sort Folder B Cheap', dummyFunction,dummyFunction)
#displayPlot('C', 'c', ['t'], 'Tim Sort Folder C Cheap', dummyFunction,dummyFunction)

'''
#expensive plots
displayPlot('A', 'e', ['i'], 'Insertion Sort Folder A Cheap', dummyFunction,dummyFunction)
displayPlot('B', 'e', ['i'], 'Insertion Sort Folder B Cheap', dummyFunction,dummyFunction)
displayPlot('C', 'e', ['i'], 'Insertion Sort Folder C Cheap', dummyFunction,dummyFunction)
displayPlot('A', 'e', ['m'], 'Merge Sort Folder A Cheap', dummyFunction,dummyFunction)
displayPlot('B', 'e', ['m'], 'Merge Sort Folder B Cheap', dummyFunction,dummyFunction)
displayPlot('C', 'e', ['m'], 'Merge Sort Folder C Cheap', dummyFunction,dummyFunction)
displayPlot('A', 'e', ['t'], 'Tim Sort Folder A Cheap', dummyFunction,dummyFunction)
displayPlot('B', 'e', ['t'], 'Tim Sort Folder B Cheap', dummyFunction,dummyFunction)
displayPlot('C', 'e', ['t'], 'Tim Sort Folder C Cheap', dummyFunction,dummyFunction)
'''