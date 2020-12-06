import fileinput
import numpy as np

def descendSlope(move_r, data, move_d=1):
    n_trees = 0
    step_r = move_r
    slope_contour_len = len(data[0][0])

    for i in range(move_d, len(data), move_d):
        move_r_mod = move_r % slope_contour_len

        assert move_r_mod < slope_contour_len
        assert move_r_mod >= 0

        if data[i][0][move_r_mod] == '#':
            n_trees += 1
            
        move_r += step_r
    return n_trees

data = [x.split() for x in ''.join(fileinput.input()).split('\n')]

# part 1
move_r = 3
mode_d = 1
print(descendSlope(move_r, data))

# part 2 how many trees are encountered (#)
move_r = [1,3,5,7,1]
move_d = [1,1,1,1,2]
n = []
for i,m in enumerate(move_r): n.append(descendSlope(m, data, move_d[i]))
    
print(np.product(np.array(n), dtype=np.float64))
