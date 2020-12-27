import fileinput
import numpy as np
import re

def gridCompare(tile_id, tiles):
    matches = []
    for i, tile in enumerate(tiles):

        comp = [tile[0,:], tile[-1,:], tile[:,0], tile[:,-1]]

        for j in range(i+1, len(tiles)):
            # compare against top row
            tilec = tiles[j]

            comp_c = [tilec[0,:], tilec[-1,:], np.flip(tilec[0,:]), np.flip(tilec[-1,:]),
                        tilec[:,0], tilec[:,-1], np.flip(tilec[:,0]), np.flip(tilec[:,-1])]

            # returns the tile compared and tile found with row index
            for c_idx, c_r in enumerate(comp):
                for cc_idx, r in enumerate(comp_c):
                    if np.array_equal(c_r, r):
                        matches.append([int(tile_id[i]), t1_key[c_idx], 
                                        int(tile_id[j]), t2_key[cc_idx]])
    
    return np.array(matches)

def singleCompare(d_tiles, tile, tiles):
    # compares tile to tiles from dictionary d_tiles
    tiles = list(set(tiles))
    if tile in tiles:
        raise ValueError('TILE IN TILES')
    m_tile = d_tiles[tile]
    comp = [m_tile[0,:], m_tile[-1,:], m_tile[:,0], m_tile[:,-1]]
    matches = []
    for t in tiles:
        tilec = d_tiles[t].copy()
        
        comp_c = [tilec[0,:], tilec[-1,:], np.flip(tilec[0,:]), np.flip(tilec[-1,:]),
                    tilec[:,0], tilec[:,-1], np.flip(tilec[:,0]), np.flip(tilec[:,-1])]
        
        for c_idx, c_r in enumerate(comp):
            for cc_idx, r in enumerate(comp_c):
                if np.array_equal(c_r, r):
                    matches.append([tile, t, t1_key[c_idx], t2_key[cc_idx]])
    
    return matches

pos_dict = {r'row1row1$|row2row2$': lambda x: np.flip(x,0), # flip y
            r'row1row1f$|row2row2f$': lambda x: np.flip(np.flip(x,0),1), # flip x, flip y
            r'row1row2f$|row2row1f$': lambda x: np.flip(x,1), # flip x
            r'row1col1$|row2col2$': lambda x: np.rot90(x,k=1),
            r'row2col1$|row1col2$': lambda x: np.flip(np.rot90(x,k=3),1),
            r'row1col1f$|row2col2f$': lambda x: np.flip(np.rot90(x,k=1),1),
            r'row2col1f$|row1col2f$|col1row1$|col2row2$': lambda x: np.rot90(x,k=3),
            r'col2row1$|col1row2$': lambda x: np.flip(np.rot90(x,k=1),0),
            r'col1col1$|col2col2$': lambda x: np.flip(x,1),
            r'col1row1f$|col2row2f$': lambda x: np.flip(np.rot90(x,k=3),0),
            r'col2row1f$|col1row2f$': lambda x: np.rot90(x,k=1),
            r'col1col1f$|col2col2f$': lambda x: np.flip(np.flip(x,1),0),
            r'col2col1f$|col1col2f$': lambda x: np.flip(x,0),
            r'col1col2$|col2col1$|row1row2$|row2row1$': lambda x: x, # do nothing
          }

def adjustTile(string, tile):
    for pattern, fn in pos_dict.items():
        m = re.match(pattern, string)
        if m: 
            return fn(tile)
    else:
        raise ValueError('No such string.')

def xyCo(str1):
    if 'row1' == str1: return np.array([0,1])
    elif 'row2' == str1: return np.array([0,-1])
    elif 'col1' == str1: return np.array([-1,0])
    elif 'col2' == str1: return np.array([1,0])
    else: raise ValueError('No such xy.')
    

d = [i.split('\n') for i in "".join(fileinput.input()).split('\n\n')]

tile_id = [re.findall(r'[0-9]+', i[0])[0] for i in d]
tiles = np.array([[[1 if k == '#' else 0 for k in list(j)] for j in i[1:]] for i in d])
d_tile = dict((tile_id[i], tiles[i]) for i in range(len(tiles)))

t1_key = ['row1', 'row2', 'col1', 'col2']
t2_key = ['row1', 'row2', 'row1f', 'row2f', 'col1', 'col2', 'col1f', 'col2f']

# part 1
matches = gridCompare(tile_id, tiles)
tile_id_match = np.sort(np.concatenate([matches[:,0], matches[:,2]]))
corner = [u for u in np.unique(tile_id_match) if (u == tile_id_match).sum()==2]
print(np.product([float(i) for i in corner]))

# part 2
# get tile positions and correct orientations
cs = [corner[0]]
n_iters = 100
edge_dir = [] 
seen = [cs[0]]
x = 0
y = 0
grid_co = {cs[0]: np.array([0,0])}
for n_iter in range(n_iters):
    # get tiles touching current tile
    tiles = [matches[matches[:,0] == c][:,2] for c in cs]
    tiles.extend([matches[matches[:,2] == c][:,0] for c in cs])
    tiles = [j for i in tiles for j in i]
    ms = [singleCompare(d_tile, c, tiles) for c in cs]
    ms = [j for i in ms for j in i]
    
    cs = []
    for from_tile, tile, str1, str2 in ms:
        if n_iter == 0:
            d_tile[tile] = adjustTile(str1+str2, d_tile[tile])
            edge_dir.append(str1)
            cs.append(tile)
            seen.append(tile)
            grid_co[tile] = grid_co[from_tile] + xyCo(str1)
                
        elif tile not in seen:
            if str1 in edge_dir:            
                d_tile[tile] = adjustTile(str1+str2, d_tile[tile])
                cs.append(tile)
                seen.append(tile)
                grid_co[tile] = grid_co[from_tile] + xyCo(str1)
                
    if len(cs) == 0:
        break

# correct co-ordinates of each tile to handle different corners
xyc = []
tile_id = []
for k, item in grid_co.items():
    xyc.append(np.array([int(item[0]), int(item[1])]))
    tile_id.append(k)

xyc = np.array(xyc)
xyc[:,0] = xyc[:,0] + np.abs(np.min(xyc[:,0]))
xyc[:,1] = xyc[:,1] - np.max(xyc[:,1])

# remove borders
d_img = d_tile.copy()
for k in d_img: 
    d_img[k] = d_img[k][1:-1, 1:-1]
    
image_size = d_img[k].shape

# initialise image
image = np.zeros([int(image_size[0]*len(d_img)**0.5), int(image_size[0]*len(d_img)**0.5)])

# populate image
for i, (k, item) in enumerate(grid_co.items()):
    c, r = np.abs(xyc[i])*image_size[0]
    image[r:r+image_size[0], c:c+image_size[1]] = d_img[tile_id[i]]

# define monster
monster = ['                  # ',
           '#    ##    ##    ###',
           ' #  #  #  #  #  #   ']

monster = np.array([[1 if i=='#' else -1 for i in list(m)] for m in monster]) # 1 if i == '#' else 0
r_m, c_m = monster.shape


# search image
max_cc = []
m_match = np.sum(monster[monster > 0])
n_m = 0

rotations = [0,1,2,3]
flips = [None,0,1]

for rot in rotations:
    image_loop = image.copy()
    image_loop = np.rot90(image_loop, k=rot)
    for fs in flips:
        if fs is not None:
            image_loop = np.flip(image_loop, axis=fs)
            
        for i in range(image_loop.shape[0]):
            for j in range(image_loop.shape[1]):
                window = image_loop[i:i+r_m, j:j+c_m]
                if window.shape[0] != r_m or window.shape[1] != c_m:
                    break
                else:
                    ccor = monster*window
                    max_cc.append(np.sum(ccor[ccor>0]))
                    if np.sum(ccor[ccor>0]) == m_match:
                        print('FOUND A MONSTER!')
                        n_m += 1


print(np.sum(image_loop) - n_m*m_match)
