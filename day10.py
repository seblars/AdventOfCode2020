import fileinput
import numpy as np

# part 1
d = np.sort(np.array([int(i) for i in " ".join(fileinput.input()).split('\n')]))
d = np.concatenate([[0], d, [d[-1]+3]])

print((((d[1:] - d[:-1]) == 3).sum())*((d[1:] - d[:-1]) == 1).sum())

# part 2
mp = np.ones(d.shape)
nways = np.ones(d.shape)
for i in range(0,len(d)-2):
    diff2 = d[i+2] - d[i]
    if diff2 <= 3:
        if diff2 == 2:    
            # feed forward multiplier
            mp[i+2:] = nways[i] + 1*mp[i]
            # calc third diff
            diff3 = d[i+3] - d[i]
            if (diff3 == 3): #  & (i < len(d2)-3)
                nways[i:] = nways[i] + 2*mp[i]
                # feed forward multiplier
                mp[i+3:] = nways[i]
            else:
                nways[i:] = nways[i] + 1*mp[i]
        
print(nways[-1])
