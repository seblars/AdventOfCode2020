def transformKey(target, subject=7, n_iter=50e6):
    val = 1
    for i in range(1,int(n_iter)+1):
        val = (val*subject) % 20201227
        if val is not None:
            if val == target:
                print('SUCCESS', val, target)
                print('Secret loopsize = ', i, target)
                return i
            
    if target is None:
        return val
    else:
        raise ValueError('Exceeded n iter')

keys = [17773298, 15530095]

loop_size = []
for target in keys:
    loop_size.append(transformKey(target))
    
print(transformKey(target=None, subject=keys[0], n_iter=loop_size[1]))
print(transformKey(target=None, subject=keys[1], n_iter=loop_size[0]))
