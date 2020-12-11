import fileinput
import numpy as np

data = [int(i) for i in "".join(fileinput.input()).split('\n')]

# part 1
def twoNumCombi(d1,d2):
    return np.array(np.meshgrid(d1, d2)).reshape(2,-1).T.sum(-1)

for i in range(25, len(data), 1):
    n = (twoNumCombi(data[i-25:i],data[i-25:i]) == data[i]).sum()
    if n < 1:
        print(data[i])
        break

# part 2
def findContiguous(data, n):
    for j in range(n):
        for k in range(j,n): 
            if sum(data[j:k]) == data[n]:
                return print(np.min(data[j:k]) + np.max(data[j:k]))

findContiguous(data, i)
