import fileinput
import re

d = "".join(fileinput.input()).split('\n')

# part 1
def emulatorV1(d, target='X', v1=True):
    mem_add = 1 if v1 else 0
    mem_dict = {}
    
    for line in d:
        mask = re.match(r'mask = ([0-1X]+)', line)
        mem = re.match(r'mem.([0-9]+). = ([0-9]+)', line)
        if mask and not mem:
            bitmask = list(mask.groups()[0])
        elif mem and not mask:
            bm_edit = bitmask.copy()
            value = "{0:b}".format(int(mem.groups()[mem_add]))
            value = list((36-len(value))*'0' + value)
            for i, bm in enumerate(bm_edit): 
                if bm == target: 
                    bm_edit[i] = value[i]
            if v1:  
                mem_dict[mem.groups()[0]] = int("".join(bm_edit),2)
            else:
                mem_dict = decoderV2(mem_dict, bm_edit, mem)
        else:
            raise ValueError('Exception!')
    
    print(sum(mem_dict.values()))

# part 2
def decoderV2(mem_dict, bm_edit, mem):
    xidx = [i for i in range(len(bm_edit)) if bm_edit[i] == 'X']

    for i in range(2**len(xidx)):
        b_string = "{0:b}".format(i) 
        b_string = (len(xidx)-len(b_string))*'0' + b_string
        b_string = list(b_string)
        for idx in range(len(xidx)):
            bm_edit[xidx[idx]] = b_string[idx]
        mem_dict["".join(bm_edit)] = int(mem.groups()[1])
    return mem_dict    

# part 1
emulatorV1(d)

# part 2
emulatorV1(d, target='0', v1=False)
