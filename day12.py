import fileinput
import numpy as np

def moveF(pos, act):
    rot = pos[2] % 360
    if rot == 0: act = 'E' + act[1:]
    elif rot == 90: act = 'N' + act[1:]
    elif rot == 180: act = 'W' + act[1:]
    elif rot == 270: act = 'S' + act[1:]
    else: raise ValueError('Unknown dir.')
        
    return moveBoat(pos, act)

def moveBoat(pos, act):
    # pos - (x, y, dir)
    move = np.zeros(3,)
    if act[0] == 'N': move[1] = int(act[1:])
    elif act[0] == 'S': move[1] = -int(act[1:])
    elif act[0] == 'E': move[0] = int(act[1:])
    elif act[0] == 'W': move[0] = -int(act[1:])
    elif act[0] == 'L': move[2] = int(act[1:])
    elif act[0] == 'R': move[2] = -int(act[1:])
    elif act[0] == 'F': return moveF(pos, act)
    else: raise ValueError('Unknown act.')
        
    return pos + move

def manhattenDist(pos):
    return np.abs(pos[0]) + np.abs(pos[1])

def rotMat(pos):
    theta = (pos[2] % 360)*np.pi/180
    rot = np.array([[np.cos(theta), -np.sin(theta)], 
                    [np.sin(theta), np.cos(theta)]])
    
    return np.concatenate([rot.dot(pos[:2]),[0]])

def moveFWP(wp, pos, act):
    mlp = int(d[i][1:])
    
    return pos + mlp*wp[:2]

d = "".join(fileinput.input()).split('\n')

# part 1
pos = np.array([0,0,0]) # x, y, dir
for i in range(len(d)): pos = moveBoat(pos, d[i])
print(manhattenDist(pos))

# part 2
wp = np.array([10,1,0]) # x, y, dir
pos = np.array([0,0]) # x, y
for i in range(len(d)):
    if d[i][0] == 'F':
        pos = moveFWP(wp, pos, d[i])
    else:
        wp = moveBoat(wp, d[i])
        wp = rotMat(wp)

print(np.round(manhattenDist(pos)))
