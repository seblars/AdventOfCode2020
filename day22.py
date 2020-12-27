import fileinput
import numpy as np

def adjustDeck(a,b):
    a.extend((a[0],b[0]))
    return a[1:], b[1:]

def calcScore(a):
    return sum(np.array(a)*np.flip(np.arange(1,len(a)+1)))

def checkRounds(a, previous):
    query = sum([True for i in previous if a == i])
    return True if query > 0 else False

def playGame(p1, p2, game_no, v2=True, verbose=False):
    p1 = p1.copy()
    p2 = p2.copy()

    if verbose:
        print('Playing game no.', game_no)
        
    winner = 0
    converged = False
    previous = []
    infinte = 0
    while not converged:
        if checkRounds(p1, previous) and v2: # check if game played previously
            winner = 1
            infinite = 1
            converged = True
        elif (p1[0] <= len(p1)-1) and (p2[0] <= len(p2)-1) and v2:# sub game            
            winner = playGame(p1[1:p1[0]+1], p2[1:p2[0]+1], game_no+1)
        else: # compare top card
            winner = 1 if p1[0] > p2[0] else 2
        # append game
        previous.append(p1)
        
        if winner == 1: 
            p1, p2 = adjustDeck(p1,p2)
        else: 
            p2, p1 = adjustDeck(p2,p1)
                
        # test for endgame
        if len(p1) == 0 or len(p2) == 0:
            converged = True
    
    if not infinte:
        winner = 2 if len(p1) == 0 else 1

    if verbose:
        print(f'Player {winner} wins game {game_no}')
    
    if game_no == 1:
        print('Score =', calcScore(p1) if winner == 1 else calcScore(p2))
            
    return winner

d = [i.split('\n') for i in "".join(fileinput.input()).split('\n\n')]
p1 = [int(i) for i in d[0][1:]]
p2 = [int(i) for i in d[1][1:]]

# part 1
playGame(p1, p2, 1, v2=False)

# part 2
playGame(p1, p2, 1, v2=True)
