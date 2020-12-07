import fileinput
import re

data = ''.join(fileinput.input()).split('\n')

def searchData(target):
    return [d for d in data if re.search(target, d) is not None]

# part 1
targets = ['shiny gold']
searched = []
all_bags = []
converged = False
while not converged:
    new_targets = []
    for t in targets:
        if t not in searched:
            # search data
            bags = searchData(t)
            bags = [" ".join(b.split()[:2]) for b in bags]
            # remove target
            while t in bags: bags.remove(t)
            
            searched.append(t)
            if len(bags) > 0:
                new_targets.extend(bags)
                all_bags.extend(bags)
        
    targets = new_targets

    if len(targets) == 0:
        converged = True

print(len(set(all_bags)))

# part 2
pattern1 = ' bags contain'
pattern2 = r'([0-9]+)\s([a-z]+\s[a-z]+)\sbag'
targets = [(1, 'shiny gold')] 

n_bags = 0
converged = False

d_bags = {}
multiplier = [1]
while not converged:
    new_targets = []
    for t in targets:
        for d in searchData(t[1] + pattern1):
            bags = d.split("contain ")[1].split(', ')
            for b in bags:
                m = re.match(pattern2, b)
                if m:
                    n_bag, type_bag = m.groups()
                    n_bags += t[0]*int(n_bag)
                    new_targets.append((t[0]*int(n_bag), type_bag))
    
    if len(new_targets) == 0:
        converged = True
    else:
        targets = new_targets

print(n_bags)
