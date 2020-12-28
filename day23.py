def linkDict(d):
    return dict((no, d[(idx + 1) % len(d)]) for idx, no in enumerate(d))

def cupGame(d, n_moves=100):
    
    d_link = linkDict(d)
    max_val = max(d)
    pos = d[0]
    
    for _ in range(n_moves):
        cup1 = d_link[pos]
        cup2 = d_link[cup1]
        cup3 = d_link[cup2]
        cup_nxt = d_link[cup3]
        cups = [cup1, cup2, cup3]
        
        destination = pos - 1
        while True:
            if destination not in cups and destination >= 1:
                break
            else:
                if destination in cups:
                    destination -= 1
                if destination < 1:
                    destination = max_val

        end_link = d_link[destination]
        d_link[pos] = cup_nxt
        d_link[destination] = cup1
        d_link[cup3] = end_link

        pos = cup_nxt
        
    return d_link

d = '459672813'
d = [int(i) for i in list(d)]

# part 1
d_link = cupGame(d)
string = ''
pos = 1
for _ in range(len(d)-1):
    string += str(d_link[pos])
    pos = d_link[pos]
print(string)

# part 2
d_p2 = d.copy() + [int(i) for i in range(int(max(d)+1), int(1e6+1))]
d_link_2 = cupGame(d_p2, n_moves=int(10e6))
print(float(d_link_2[1])*float(d_link_2[d_link_2[1]]))
