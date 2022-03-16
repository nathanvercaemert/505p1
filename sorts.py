def insertionSort(ar):
    for i in range(1, len(ar)):
        j = i
        while 0 < j and ar[j] < ar[j - 1]:
            ar[j - 1], ar[j] = ar[j], ar[j - 1]
            j -= 1


def merge(l, r):
    s = []
    i, j = 0, 0
    while i < len(l) and j < len(r):
        if l[i] < r[j]:
            s.append(l[i])
            i += 1
        else:
            s.append(r[j])
            j += 1
    while i < len(l):
        s.append(l[i])
        i += 1
    while j < len(r):
        s.append(r[j])
        j += 1
    return s


def mergeSort(ar):
    if len(ar) < 2:
        return ar[:]
    else:
        m = int(len(ar) / 2)
        l = mergeSort(ar[:m])
        r = mergeSort(ar[m:])
        return merge(l, r)
