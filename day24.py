import fileinput
import numpy as np
import collections
import re

def splitString(s):
    offset = 0
    diags = ['se', 'sw', 'ne', 'nw']
    pattern = diags[0]+'|'+diags[1]+'|'+ diags[2] +'|'+diags[3]
    for m in re.finditer(pattern, s):
        idxs = m.start() + offset
        s = s[:idxs] + ',' + s[idxs:]
        offset += 1
        
        idxe = m.end() + offset
        s = s[:idxe] + ',' + s[idxe:]
        offset += 1

    s = [[i] if i in diags else list(i) for i in s.split(',') if i != '']
    return [j for i in s for j in i]

def findTile(seq):
    pos = np.array([0,0])
    for act in seq:
        pos = tuple(np.round(d_move[act](pos),3))
    
    return pos

def hexNN(pos):
    # determine nearest tiles
    nearest = []
    for k in d_move:
        nn = tuple(np.round(d_move[k](pos),3))
        nearest.append(nn)
    
    return nearest

def determineMove(idx, tile_col, grid):
    
    pos = grid[idx]
    state = tile_col[idx]
    
    n_black = sum([tile_col[grid.index(n)] for n in hexNN2(pos, grid)])
    if (state == 1) and (n_black == 0 or n_black > 2):
        move = 0
    elif (state == 0) and (n_black == 2):
        move = 1
    else:
        move = state
    
    return move

d_move = {'ne': lambda x: x + np.array([1., 3.**0.5]),
          'e': lambda x: x + np.array([2.,0]),
          'se': lambda x: x + np.array([1., -3.**0.5]),
          'sw': lambda x: x + np.array([-1., -3.**0.5]),
          'w': lambda x: x + np.array([-2.,0]),
          'nw': lambda x: x + np.array([-1., 3.**0.5]),
        }

d = "".join(fileinput.input()).split('\n')
d = [splitString(i) for i in d]

# part 1
d_flip = [findTile(seq) for seq in d]
double_flip = [item for item, count in collections.Counter(d_flip).items() if count > 1]
black_tiles = list(set(d_flip) ^ set(double_flip))
print(len(black_tiles))

# part2 - v.slow
for i in range(100):
    
    new_tiles = set()
    
    # make the grid
    grid = black_tiles.copy()
    for tile in black_tiles:
        grid.extend(hexNN(tile))

    grid = list(set(grid))
    
    for tile in grid:
        n_black = sum(n in black_tiles for n in hexNN(tile))
        
        if tile in black_tiles:
            if (n_black == 1) or (n_black == 2):
                new_tiles.add(tile)
        else:
            if n_black == 2:
                new_tiles.add(tile)
    
    black_tiles = list(new_tiles)
    
print(len(black_tiles))
