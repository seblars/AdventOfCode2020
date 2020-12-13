import fileinput
import numpy as np

def adj(x, nrows, ncols, n=1): 
        pos_adj = [(x[0]+n, x[1]), (x[0]+n, x[1]+n), (x[0], x[1]+n), (x[0]-n, x[1]+n), 
                       (x[0]-n, x[1]), (x[0]-n, x[1]-n), (x[0], x[1]-n), (x[0]+n, x[1]-n)]
        
        for i in range(len(pos_adj)):
            if pos_adj[i][0] < 0 or pos_adj[i][1] < 0:
                pos_adj[i] = None
            elif pos_adj[i][0] >= nrows or pos_adj[i][1] >= ncols:
                pos_adj[i] = None
        
        return [i for i in pos_adj if i]
    
def simulate(d, adj_seats, tolerance=3):
    d_new = d.copy()
    for i in range(d.shape[0]):
        for j in range(d.shape[1]):
            n_oc = np.sum([1 for a in adj_seats[i,j] if d[a] == '#'])
            if (d[i,j] == 'L') & (n_oc == 0):
                d_new[i,j] = '#'
            elif (d[i,j] == '#') & (n_oc > tolerance):
                d_new[i,j] = 'L'
    
    return d_new

def simLoop(d, adj_seats, tol=3):
    d_sim = d.copy()
    n_sims = 100
    n_oc = 0
    n_oc_prev = -100

    for i in range(n_sims):
        d_sim = simulate(d_sim, adj_seats, tolerance= tol)
        n_oc = np.sum([1 for i in d_sim.ravel() if i == '#'])
        if n_oc - n_oc_prev == 0:
            print(f'converged with {i-1} sims, occupancy= {n_oc}')
            break
        n_oc_prev = n_oc

def vectorSearch(d, seat_coor, i, j, d_search=25):
    for k, a in enumerate(seat_coor):
        if d[a] == '.':
            v = np.array(a)-np.array([i,j])

            for n_v in range(1,d_search):
                vec = tuple(np.array([i,j])+n_v*v)

                if (vec[0] >= d.shape[0]) or (vec[1] >= d.shape[1]):
                    seat_coor[k] = None
                    break
                elif (vec[0] < 0) or (vec[1] < 0):
                    seat_coor[k] = None
                    break

                if d[vec] == '#' or d[vec] == 'L':
                    seat_coor[k] = vec
                    break

    return [sc for sc in seat_coor if sc]

d = np.array([np.array(list(i)) for i in ''.join(fileinput.input()).split('\n')])

# part 1
adj_seats = [adj((i,j), *d.shape) for i in range(d.shape[0]) for j in range(d.shape[1])]
adj_seats = np.array(adj_seats).reshape(d.shape)
simLoop(d, adj_seats, tol=3)

# part 2
adj_seats = [vectorSearch(d, adj_seats[i,j], i, j) for i in range(d.shape[0]) for j in range(d.shape[1])]
adj_seats = np.array(adj_seats).reshape(d.shape)
simLoop(d, adj_seats, tol=4)
