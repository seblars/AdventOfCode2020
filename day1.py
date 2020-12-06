import fileinput
a = [int(x) for x in ''.join(fileinput.input()).split('\n')]

# part 1
target = 2020 

for i in range(len(a)):
    for j in range(i+1, len(a)):
        if a[i] + a[j] == target:
            print('Found target a:', a[i]*a[j])

# part 2
for i in range(len(a)):
    for j in range(i+1, len(a)):
        for k in range(j+1, len(a)):
            if a[i] + a[j] + a[k] == target:
                print('Found target b:', a[i]*a[j]*a[k])
