import fileinput
import re

def getInsertion(line, matches):
    level_idx = [0]
    new_line = []
    for m in matches:
        if m.group() == '(':
            level_idx.append(m.start())
        elif m.group() == ')':
            del level_idx[-1]
        elif m.group() == '*':
            new_line.append((level_idx[-1], '('))
            new_line.append((m.start(), ')'))
            
    return sorted(new_line)

def getInsertionV2(line, matches):
    level_idx = [0]
    new_line = []
    for m in matches:
        if m.group() == '*':
            li = level_idx[-1]
            new_line.append((li, '('))
            new_line.append((m.start(), ')'))
            level_idx.append(m.start()+1)
            
    new_line.append((level_idx[-1], '('))
    new_line.append((len(line), ')'))
            
    return sorted(new_line)

def insertToList(line, v1=True):
    matches = [m for m in re.finditer(r'\*|\(|\)', line)]
    if v1:
        insertion = getInsertion(line, matches)
    else:
        insertion = getInsertionV2(line, matches)
        
    nd = list(line)
    [nd.insert(i+ins[0],ins[1]) for i,ins in enumerate(insertion)]
    return "".join(nd)

d = "".join(fileinput.input()).split('\n')

# part 1
print(sum([eval(insertToList(line)) for line in d]))

# part 2
print(sum([eval(insertToList(line, v1=False)) for line in d]))
