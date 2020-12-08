import fileinput
import numpy as np

def test_loop(d, verbose=True):
    i = 0
    acc = 0
    not_converged = True
    first_idx = []
    while not_converged:
        first_idx.append(i)
        line = d[i]

        if line[0] == 'acc':
            acc += int(line[1])
            i += 1
        elif line[0] == 'jmp':
            i += int(line[1])
        elif line[0] == 'nop':
            i += 1
        else:
            raise ValueError('Input not recognised')
        
        if len(set(first_idx)) < len(first_idx):
            not_converged = False
            if verbose:
                print('Infinite loop', acc - int(line[1]))
        elif i > len(d):
            not_converged = False
        else:
            if i == len(d):
                not_converged = False
                print('Successful boot', acc)
                return True
            
    return False

d = [d.split() for d in ''.join(fileinput.input()).split('\n')]

# part 1
test_loop(d)

# part 2
nopsjmps = np.arange(0,len(d))[(np.array(d)[:,0] == 'nop') | (np.array(d)[:,0] == 'jmp')]

for nj in nopsjmps:
    d_delta = [ds[:] for ds in d]
    if d_delta[nj][0] == 'nop':
        d_delta[nj][0] = 'jmp'
    elif d_delta[nj][0] == 'jmp':
        d_delta[nj][0] = 'nop'
    
    if test_loop(d_delta, verbose=False):
        break
