import fileinput
# "day6.txt"
groups = [x.split() for x in ''.join(fileinput.input()).split('\n\n')]

# part 1
print(sum(len(set([j for sub in group for j in sub])) for group in groups))

# part 2
print(sum(len(set.intersection(*[set(list(j)) for j in group])) for group in groups))
