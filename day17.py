import numpy as np
import fileinput

d = np.array([[1 if j == '#' else 0 for j in list(i)]
              for i in "".join(fileinput.input()).split('\n')])

def sumNN(d, idx):
    return np.sum(d[tuple([slice(i-1,i+2) for i in idx])])
    
def cubeConv(d, n_cycles=6):

    for _ in range(n_cycles):
        d = np.pad(d,1)
        d_new = d.copy()
        mg = [np.arange(1,i-1) for i in d.shape]
        ind = np.array([i.ravel() for i in np.meshgrid(*mg)]).T

        for idx in ind:
            idx = tuple(idx)
            nn = sumNN(d,idx)
            if (d[idx] == 1) & (nn < 3) | (nn > 4):
                d_new[idx] = 0
            elif (d[idx] == 0) & (nn == 3):
                d_new[idx] = 1

        d = d_new.copy()
        
    print(d.sum())

# part 1
d1 = np.pad(d.reshape(1,*d.shape),1)
cubeConv(d1)

# part 2
d2 = np.pad(d.reshape(*([1]*2),*d.shape), 1)
cubeConv(d2)
