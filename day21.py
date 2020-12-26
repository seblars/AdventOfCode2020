import fileinput
import re

d = "".join(fileinput.input()).split('\n')
allergens = [i[re.search(' \(contains ', i).end():i.find(")")] for i in d]
allergens = [i.split(', ') for i in allergens]
ingredients = [i[:re.search(' \(contains ', i).start()] for i in d]
ingredients = [i.split() for i in ingredients]

# part 1
allergen_list = list(set([j for i in allergens for j in i]))
d_allergen = dict((i, []) for i in allergen_list)
for al in allergen_list:           
    d_allergen[al] = [i for i, allergen in enumerate(allergens) if al in allergen]
    d_allergen[al] = list(set.intersection(*[set(ingredients[i]) for i in d_allergen[al]]))
    
ingredient_list = [j for i in ingredients for j in i]
allergic_candidates = set([j for i in d_allergen.values() for j in i])
safe_ingredients = list(set(ingredient_list).symmetric_difference(set(allergic_candidates)))
print(sum([ingredient_list.count(si) for si in safe_ingredients]))

# part 2
order = []
match = []
converged = False
while not converged:
    n_vs = 0
    for k, v in d_allergen.items():
        if k not in match:
            d_allergen[k] = [i for i in d_allergen[k] if i not in order]
            if len(v) > 1: 
                n_vs += 1
            else:
                order.extend(v)
                match.append(k)

    if n_vs == 0:
        converged = True
        
canonical = [i[1][0] for i in sorted([(k,v) for k,v in d_allergen.items()])]
print ("",'%s'%','.join(map(str, canonical))) 
