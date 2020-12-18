def lastSpoken(d, n=2020):
    
    d_l = dict([(d[i], i+1) for i in range(len(d)-1)])
    ls = [d[-2], d[-1]]
    
    for i in range(len(d)+1, n+1):
        last_spoken = ls[1]
        if last_spoken in d_l and (last_spoken != ls[0]):
            ls[0] = last_spoken
            ls[1] = i - 1 - d_l[last_spoken]
            d_l[last_spoken] = i-1
        elif ls[1] == ls[0]:
            d_l[last_spoken] = i-1
            ls[1] = 1
        else:
            d_l[last_spoken] = i-1
            ls[0], ls[1] = last_spoken, 0
            
    print(ls[1])

d = [6,19,0,5,7,13,1]
    
# part 1
lastSpoken(d)
    
# part 2
lastSpoken(d, n=30000000)
