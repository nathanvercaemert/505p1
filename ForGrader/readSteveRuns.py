from cProfile import label
import os
from unicodedata import name
from matplotlib import style
from numpy import dtype
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import scipy.optimize as opt
from scipy.optimize import curve_fit

# folder relative to current location
directory = "./output/"
# should find all files in the directory folder
file_list = os.listdir(directory)

df = pd.DataFrame()

# append all files into 1 dataframe
for file in file_list:
    data = pd.read_csv(directory + file, names=["sortType", "cost", "file", "sorted", "preProcessTime", "sortTime"])
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
    return a * x * np.log2(x) + b * x + c

def displayPlot(folder, cost, sortTypeList, plotTitle, funcToApplySize, funcToApplyTime, curveFitBool):
    plt.clf()
    p =  dfs.loc[(dfs['folder'] == folder) & (dfs['cost'] == cost)]
    p = p.explode(['sizeList', 'timeList'], ignore_index=True)
    p['sizeList'] = p['sizeList'].astype(int)
    p['timeList'] = p['timeList'].astype(float)
    p['sizeList'] = p['sizeList'].apply(funcToApplySize)
    p['timeList'] = p['timeList'].apply(funcToApplyTime)
    for sortType in sortTypeList:
        x = p.loc[p['sortType'] == sortType]['sizeList']
        y = p.loc[p['sortType'] == sortType]['timeList']

        if curveFitBool:
            plt.scatter(x, y, label=sortType)
            f = None
            lbl = ''
            # # The actual curve fitting happens here
            if sortType == 'i':
                f = quadraticCurveFit
                lbl = 'fit: %.2ex^2 + %.2ex + %.2e'
            else :
                f = nLogNCurveFit
                lbl = 'fit: %.2exlog(x) + %.2ex + %.2e'

            optimizedParameters, _ = opt.curve_fit(f , x, y)
            # Use the optimized parameters to plot the best fit
            plt.plot(x, f(x, *optimizedParameters), label=lbl % tuple(optimizedParameters))
        else:
            plt.plot(x, y, label=sortType)
    plt.xlabel('log(size)')
    plt.ylabel('log(time) (sec)')
    #plt.xlabel(f'log(size)')
    #plt.ylabel(f'time (sec)')
    plt.ticklabel_format(style='plain')
    plt.legend()
    plt.title(plotTitle)
    plt.savefig(f'./plots/{plotTitle}.png')
    plt.show()

def dummyFunction(s):
    return s

def logFunctionS(s):
    return math.log(s, 2)

def logFunctionT(s):
    return math.log(s + 1, 2)

# predict for n^2
def predictNSq(i, j, time):
    return time / (i**2 / j**2)

def predictNLogN(i, j, time):
    return time / ( (i * math.log(i, 2)) / (j * math.log(j, 2)) )

def predictionPlot(folder, cost, sortType, plotTitle, predictFunction, f, f2):
    plt.clf()
    p =  dfs.loc[(dfs['folder'] == folder) & (dfs['cost'] == cost) & (dfs['sortType'] == sortType)]
    p = p.explode(['sizeList', 'timeList'], ignore_index=True)
    p['sizeList'] = p['sizeList'].astype(int)
    p['timeList'] = p['timeList'].astype(float)
    # plot the real list
    plt.plot(p['sizeList'].apply(f), p['timeList'].apply(f2), label='real', lw=3)
    
    # predicting up to max
    max = 4194304
    # start at first timed item
    i = 2
    while i < max:
        idx = int(math.log(i, 2))
        if (idx >= len(p)):
            break
        lst = p[idx:idx + 1]
        timeValue = lst.iloc[0]['timeList']
        # predict next item up to end
        j = i * 2
        
        while j <= max:
            lst = pd.concat([lst, pd.DataFrame([{'sortType':sortType,
                                                 'cost':cost,
                                                 'folder':folder,
                                                 'sizeList':j,
                                                 'timeList':predictFunction(i, j, timeValue)}])])
            j *= 2
        plt.plot(lst['sizeList'].apply(f), lst['timeList'].apply(f2), '--', marker='*', lw=.3 ,label=i, markevery=[0], markersize=4)
        i *= 4
    
    plt.xlabel('size')
    plt.ylabel('time (sec)')
    plt.ticklabel_format(style='plain')
    plt.legend()
    plt.title(plotTitle)
    plt.savefig(f'./plots/{plotTitle}.png')
    plt.show()

displayPlot('B', 'c', ['i', 'm', 't'], 'Folder B Log-Log Cheap', logFunctionS, logFunctionS, False)
