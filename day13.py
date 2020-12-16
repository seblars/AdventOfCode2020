import fileinput
import numpy as np

d = [i.split(',') for i in ''.join(fileinput.input()).split('\n')]

# part 1
arrival = int(d[0][0])
busses = np.array([(i,int(var)) for i,var in enumerate(d[1]) if var.isdigit()])

for i in range(100):
    t_diff_mask = np.array([(arrival+i) % b for b in busses[:,1]]) == 0
    if np.sum(t_diff_mask): break

print(busses[t_diff_mask,1]*i)

# part 2
mp = 1.
t = 0
for i in range(len(busses)-1):
    idx = busses[i+1][0]
    b_id = busses[i+1][1]
    mp *= busses[i,1]
    while (t + idx) % b_id != 0: 
        t += mp
print(t)
