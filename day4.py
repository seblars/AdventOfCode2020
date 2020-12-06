import fileinput
import re

# part 1
req = set(['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'])
pps = [x.split() for x in ''.join(fileinput.input()).split('\n\n')]
pps = [dict(x.split(':') for x in pp) for pp in pps]
print(sum(set(pp).issuperset(req) for pp in pps))

# part 2
pp_fields = {
    'byr': (r'^([12][09]\d{2})', lambda x: 1920 <= int(x) and int(x) <= 2002),
    'iyr': (r'^(20\d{2})', lambda x: 2010 <= int(x) and int(x) <= 2020),
    'eyr': (r'^(20\d\d)', lambda x: 2020 <= int(x) and int(x) <= 2030),
    'hgt': (r'^(\d{2,3})(in|cm)', lambda x, u: 59 <= int(x) <= 76 if u == 'in' else 150 <= int(x) <= 193),
    'hcl': (r'^(#[a-f0-9]{6})', lambda x: True),
    'ecl': (r'^(amb|blu|brn|gry|grn|hzl|oth)', lambda x: True),
    'pid': (r'^(\d{9})$', lambda x: True),
}

n_valid = 0
for pp in pps:
    n = 0
    for key, (pattern, fn) in pp_fields.items():
        pp_key = pp.get(key, '')
        matches = re.search(pattern, pp_key)

        if matches is not None:
            if fn(*matches.groups()):
                n += 1
    
    if n == 7:
        n_valid += 1
        
print(n_valid)
