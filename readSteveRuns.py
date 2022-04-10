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
    plt.xlabel(f'log(size)')
    plt.ylabel(f'log(time) (sec)')
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
    return math.log(s)

def logFunctionT(s):
    return math.log(s + 1)

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
    
    plt.xlabel('log(size)')
    plt.ylabel('log(time) (sec)')
    plt.ticklabel_format(style='plain')
    plt.legend()
    plt.title(plotTitle)
    plt.savefig(f'./plots/{plotTitle}.png')
    plt.show()

# displayPlot('A', 'c', ['i', 'm', 't'], 'Folder A Log-Log Cheap', logFunctionS, logFunctionS, False)
# displayPlot('B', 'c', ['i', 'm', 't'], 'Folder B Log-Log Cheap', logFunctionS, logFunctionS, False)
# displayPlot('C', 'c', ['i', 'm', 't'], 'Folder C Log-Log Cheap', logFunctionS, logFunctionS, False)
# displayPlot('A', 'e', ['i', 'm', 't'], 'Folder A Log-Log Expensive', logFunctionS, logFunctionS, False)
# displayPlot('B', 'e', ['i', 'm', 't'], 'Folder B Log-Log Expensive', logFunctionS, logFunctionS, False)
# displayPlot('C', 'e', ['i', 'm', 't'], 'Folder C Log-Log Expensive', logFunctionS, logFunctionS, False)


# displayPlot('A', 'c', ['i'], 'Folder A Cheap Insertion', dummyFunction, dummyFunction, True)
# displayPlot('A', 'c', ['m'], 'Folder A Cheap Merge', dummyFunction, dummyFunction, True)
# displayPlot('A', 'c', ['t'], 'Folder A Cheap Tim', dummyFunction, dummyFunction, True)
# displayPlot('B', 'c', ['i'], 'Folder B Cheap Insertion', dummyFunction, dummyFunction, True)
# displayPlot('B', 'c', ['m'], 'Folder B Cheap Merge', dummyFunction, dummyFunction, True)
# displayPlot('B', 'c', ['t'], 'Folder B Cheap Tim', dummyFunction, dummyFunction, True)
# displayPlot('C', 'c', ['i'], 'Folder C Cheap Insertion', dummyFunction, dummyFunction, True)
# displayPlot('C', 'c', ['m'], 'Folder C Cheap Merge', dummyFunction, dummyFunction, True)
# displayPlot('C', 'c', ['t'], 'Folder C Cheap Tim', dummyFunction, dummyFunction, True)

# displayPlot('A', 'e', ['i'], 'Folder A Expensive Insertion', dummyFunction, dummyFunction, True)
# displayPlot('A', 'e', ['m'], 'Folder A Expensive Merge', dummyFunction, dummyFunction, True)
# displayPlot('A', 'e', ['t'], 'Folder A Expensive Tim', dummyFunction, dummyFunction, True)
# displayPlot('B', 'e', ['i'], 'Folder B Expensive Insertion', dummyFunction, dummyFunction, True)
# displayPlot('B', 'e', ['m'], 'Folder B Expensive Merge', dummyFunction, dummyFunction, True)
# displayPlot('B', 'e', ['t'], 'Folder B Expensive Tim', dummyFunction, dummyFunction, True)
# displayPlot('C', 'e', ['i'], 'Folder C Expensive Insertion', dummyFunction, dummyFunction, True)
# displayPlot('C', 'e', ['m'], 'Folder C Expensive Merge', dummyFunction, dummyFunction, True)
# displayPlot('C', 'e', ['t'], 'Folder C Expensive Tim', dummyFunction, dummyFunction, True)


predictionPlot('A', 'c', 'i', 'Prediction A Cheap Insertion', predictNSq, logFunctionS, logFunctionS)
predictionPlot('B', 'c', 'i', 'Prediction B Cheap Insertion', predictNSq, logFunctionS, logFunctionS)
predictionPlot('C', 'c', 'i', 'Prediction C Cheap Insertion', predictNSq, logFunctionS, logFunctionS)
predictionPlot('A', 'c', 'm', 'Prediction A Cheap Merge', predictNLogN, logFunctionS, logFunctionS)
predictionPlot('B', 'c', 'm', 'Prediction B Cheap Merge', predictNLogN, logFunctionS, logFunctionS)
predictionPlot('C', 'c', 'm', 'Prediction C Cheap Merge', predictNLogN, logFunctionS, logFunctionS)
predictionPlot('A', 'c', 't', 'Prediction A Cheap Tim', predictNLogN, logFunctionS, logFunctionS)
predictionPlot('B', 'c', 't', 'Prediction B Cheap Tim', predictNLogN, logFunctionS, logFunctionS)
predictionPlot('C', 'c', 't', 'Prediction C Cheap Tim', predictNLogN, logFunctionS, logFunctionS)
predictionPlot('A', 'e', 'i', 'Prediction A Expensive Insertion', predictNSq, logFunctionS, logFunctionS)
predictionPlot('B', 'e', 'i', 'Prediction B Expensive Insertion', predictNSq, logFunctionS, logFunctionS)
predictionPlot('C', 'e', 'i', 'Prediction C Expensive Insertion', predictNSq, logFunctionS, logFunctionS)
predictionPlot('A', 'e', 'm', 'Prediction A Expensive Merge', predictNLogN, logFunctionS, logFunctionS)
predictionPlot('B', 'e', 'm', 'Prediction B Expensive Merge', predictNLogN, logFunctionS, logFunctionS)
predictionPlot('C', 'e', 'm', 'Prediction C Expensive Merge', predictNLogN, logFunctionS, logFunctionS)


#predictionPlot('A', 'c', 'i', 'A Cheap Insertion Prediction', predictNSq, logFunctionS, logFunctionS)
#predictionPlot('A', 'c', 'm', 'A Cheap Merge Prediction', predictNLogN, logFunctionS, logFunctionS)
#predictionPlot('A', 'e', 'i', 'A Expensive Insertion Prediction', predictNSq, logFunctionS, logFunctionS)
#predictionPlot('A', 'e', 'm', 'A Expensive Merge Prediction', predictNLogN, logFunctionS, logFunctionS)