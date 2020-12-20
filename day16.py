import fileinput
import re
import numpy as np

def validity(x, field):
    if (field[0] <= x <= field[1]) or (field[2] <= x <= field[3]):
        return True
    else:
        return False

def findError(nearby):
    error = 0
    discard = []
    t_idx = dict((i, []) for i in range(len(nearby[0])))
    
    for i, ticket in enumerate(nearby):

        assert len(ticket) == len(fields)
        
        for j, t in enumerate(ticket):
            n = 0
            for k, m in enumerate(fields):
                if not validity(t, m):
                    n += 1
                    t_idx[j].append(k)

            if n == len(fields): 
                error += t
                discard.append(i)

    print(error)
    return t_idx, discard

d = [i.split('\n') for i in "".join(fileinput.input()).split('\n\n')]

pattern = ': ([0-9]+)-([0-9]+) or ([0-9]+)-([0-9]+)' #([0-9]+)-([0-9]+) or ([0-9]+)-([0-9]+)
fields = [[int(i) for i in re.search(pattern, i).groups()] for i in d[0]]
myticket = np.array([float(i) for i in d[1][1].split(',')])
nearby = [[int(j) for j in i.split(',')] for i in d[2][1:]]


# part 1
_, discard = findError(nearby)
nearby = [x for i, x in enumerate(nearby) if i not in discard]

# part 2
d_notin, _ = findError(nearby)
lens = np.array([(k,len(d_notin[k])) for k in d_notin])
lens = lens[np.argsort(lens[:,1])]

arr = np.arange(0, len(fields))
struct = []
mapping = []
for k in reversed(lens[:,0]):   
    output = [i for i in arr if i not in d_notin[k] and i not in struct]
    struct.append(output)
    mapping.append((k, output[0]))

mapping = np.array(mapping)
mapping = mapping[np.argsort(mapping[:,1])]
print(np.prod(myticket[mapping[:,0]][:6]))
