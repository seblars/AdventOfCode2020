import fileinput
import numpy as np
data = ''.join(fileinput.input()).split('\n')

# part 1
outputs = []
row_quadrants = np.power(2, np.flip(np.arange(0,7)))
col_quadrants = np.power(2, np.flip(np.arange(0,3)))
    
for i in range(len(data)):
    row_chars = np.array([i for i in data[i][:7]])
    col_chars = np.array([i for i in data[i][7:]])

    r, c = row_quadrants[row_chars == 'B'].sum(), col_quadrants[col_chars == 'R'].sum()
    sID = r*8 + c
    
    outputs.append([sID, r, c])
#     print(sID, r, c)
    
outputs = np.array(outputs)

print(np.max(outputs[:,0]))

# part 2
idx = np.argmax(np.sort(outputs[:,0])[1:] - np.sort(outputs[:,0])[:-1])
print(np.sort(outputs[:,0])[idx] + 1) # , np.sort(outputs[:,0])[idx+1]
