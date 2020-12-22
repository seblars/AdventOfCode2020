import fileinput
import re

def convertKey(keys, orb=0):
    
    m1 = re.search(r'([0-9]+) ([0-9]+) \| ([0-9]+) ([0-9]+)\s?$', keys)
    m2 = re.search(r'([0-9]+) \| ([0-9]+)\s?$', keys)
    m3 = re.search(r'([0-9]+) ([0-9]+)', keys)
    m4 = re.search(r'([0-9]+)', keys)
    m5 = re.search(r'([a-b])', keys)

    if m1: keys = m1.groups()
    elif m2: keys = m2.groups()          
    elif m3: keys = m3.groups()
    elif m4: keys = m4.groups()
    elif m5: keys = m5.groups()
    else: raise ValueError('No key match.')

    return keys

def flattenDict(d_dict, init_string ='0'):
    
    string = ' ' + d_dict[init_string] + ' '
    new_string = [string]
    for counter in range(100):
        new_search = [convertKey(i) for i in new_string]
        new_search = [item for sublist in new_search for item in sublist]
#         print(new_search)
        if re.search(r'[0-9]', "".join(new_search)):
            new_string = [s if s =='a' or s =='b' else d_dict[s] for s in new_search]
            ns = [s if s =='a' or s =='b' else ' ( '+s+' ) ' for s in new_string]
            
            for i in range(len(new_search)):
                string = string.replace(' '+new_search[i]+' ', ' '+ns[i]+' ')
#             print(string, '\n')
        else:
            print(f'Converged in {counter}.')
            break

    string = string.replace(' ', '')
    string = string.replace('"b"', 'b')
    string = string.replace('"a"', 'a')
    
    return string

def queryString(string, messages, v1=True):
    n_true = 0
    pattern = re.compile(string)
    for term in messages:
        m = re.match(pattern, term)
        if m:
            if v1:
                if len(m.group()) == len(term):
                    n_true += 1
            else:
                n_true += 1               

    print(n_true)

d = [i.split('\n') for i in "".join(fileinput.input('day19.txt')).split('\n\n')]
d_dict = dict([tuple(i.split(': ')) for i in d[0]])

# part 1
string = flattenDict(d_dict)
queryString(string, d[1])

# part 2 - to-do
string1 = flattenDict(d_dict,  init_string='42')
string2 = flattenDict(d_dict,  init_string='31')
queryString('^(' + string1 + '){2,}(' + string2 + '){1,}$', d[1], v1=False)


