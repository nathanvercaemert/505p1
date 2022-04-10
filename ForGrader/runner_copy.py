import os
import sys
import math

def print_error(string):
    print(string)
    print()
    exit()

def run_sort(in_file, out_file, type, cost, log_file, num):
    #for i in range(num):
    os.system(f'python3 ./main.py {in_file} {out_file} {type} {cost} {num} >> {log_file}')
    last_line = ""
    # read the time from the last line and predict the next run
    with open(log_file, 'r') as f:
        last_line = f.readlines()[-1]
    # maybe predict out to max file size too, to see how accuracy improves
    last_line = last_line.strip().split(',')[-1]
    return float(last_line)

def directory_sort(type, cost, output_name):
    # go through all directories that match
    for dirs in directory_list:
        for dir in dirs:
            # run on given or all directories
            if sort_directory == "ALL" or dir == sort_directory:
                files = os.listdir(directory + dir)
                files.sort(key=lambda x: int(os.path.splitext(x)[0]))
                x = 1.0
                # 3 warmups and 10 runs
                runs = 13
                for file in files:
                    if x >= 128:
                        break
                        # 2 warmups and 3 runs
                        runs = 5
                    # run the sort on each file, a number of times
                    run_time = run_sort(directory + dir + '/' + file, out_file_base + "sorted_" + type + cost + dir + file, type, cost, log_file_base + output_name, runs)
                    # try to cut off if the run gets too long
                    if type == 'i' and run_time / (.25) > sort_time_cap:
                        break
                    elif (x > 2 and (type == 'm' or type == 't')) and run_time / ( (x * math.log(x, 2)) / (x * 2 * math.log(x * 2, 2)) ) > sort_time_cap:
                        break
                    x *= 2

# make sure correct number of arguments or print usage
if len(sys.argv) != 5:
    print_error("usage: python3 runner_copy [A|B|C|ALL] [i|m|t|ALL] [c|e|ALL] <int>")

# A, B, or C
sort_directory=sys.argv[1]
# i = insertion, m = merge, t = tim, a = all
sort_type=sys.argv[2]
# c = cheap, e = expensive, b = both
sort_cost=sys.argv[3]
# time cap per single run
sort_time_cap=sys.argv[4]

# if not A, B, or C, print usage highlighting that
if sort_directory not in {"A", "B", "C", "ALL"}:
    print_error("usage: python3 runner_copy " + '\033[1m' +  "[A|B|C|ALL]" + '\033[0m' +  " [i|m|t|ALL] [c|e|ALL] <int>")

# check if the sort type is i, m, or t, print usage highlighting that if it is wrong
if sort_type not in {"i", "m", "t", "ALL"}:
    print_error("usage: python3 runner_copy [A|B|C|ALL] " + '\033[1m' + "[i|m|t|ALL]" + '\033[0m' + " [c|e|ALL] <int>")

# check if the sort type is i, m, or t, print usage highlighting that if it is wrong
if sort_cost not in {"c", "e", "ALL"}:
    print_error("usage: python3 runner_copy [A|B|C|ALL] [i|m|t|ALL] " + '\033[1m' + "[c|e|ALL]" + '\033[0m' + " <int>")

if not sort_time_cap.isnumeric():
    print_error("usage: python3 runner_copy [A|B|C|ALL] [i|m|t|ALL] [c|e|ALL] " + '\033[1m' + "<int>" + '\033[0m')

sort_time_cap = int(sort_time_cap)

# get the directory
# directory = '/root/csc505-spring-2022/Project1/'
directory = './../csc505-spring-2022/Project1/'
directory_list = os.listdir(directory)
out_file_base = "./sorted/"
log_file_base = "./output/"

if sort_cost == "ALL" or sort_cost == "c":
    if sort_type == "ALL" or sort_type == "i":
        directory_sort("i", "c", "InsertionSortCheap.log")
    
    # run merge sort
    if sort_type == "ALL" or sort_type == "m":
        directory_sort("m", "c", "MergeSortCheap.log")

    # run tim sort
    if sort_type == "ALL" or sort_type == "t":
        directory_sort("t", "c", "TimSortCheap.log")

if sort_cost == "ALL" or sort_cost == "e":
    if sort_type == "ALL" or sort_type == "i":
        directory_sort("i", "e", "InsertionSortExpensive.log")

    # run merge sort
    if sort_type == "ALL" or sort_type == "m":
        directory_sort("m", "e", "MergeSortExpensive.log")
