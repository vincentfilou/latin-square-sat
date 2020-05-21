def build_and(left, right):
    return {'type':'and','left':left,'right':right}

def build_or(left,right):
    return {'type':'or','left':left,'right':right}

def build_atom(atom):
    return {'type':'atom','atom':atom}

def equal(p0,p1):
    if p0['type'] == p1['type']:
        if p1['type'] == 'atom':
            return p0['atom'] == p1['atom']
        else: 
            return equal(p0['left'],p1['left']) and equal(p0['right'],p1['right'])
    else:
        return False

def normalize1(p):
    if p['type'] == 'atom':
        return p
    else:
        a = normalize1(p['left'])
        b = normalize1(p['right'])
        if p['type'] == 'or':
            if b['type'] == 'and':
                return build_and(build_or(a,b['left']), build_or(a,b['right']))
            else:
                if a['type'] == 'and':
                    return build_and(build_or(a['left'],b), build_or(a['right'],b))
                else:
                    return build_or(a,b)
        else:
            return build_and(a,b)


def normalize(p):
    p0 = normalize1(p)
    while equal(p0,p) == False:
        p = p0
        p0 = normalize1(p)
    return p0
    
def big_and(t,f):
    if len(t) == 1:
        return f(t[0])
    else:
        return build_and(big_and(t[0:1],f),big_and(t[1:],f))

def big_or(t,f):
    if len(t) == 1:
        return f(t[0])
    else:
        return build_or(big_or(t[0:1],f),big_or(t[1:],f))

def to_clauses(t):
    if t['type'] == "atom":
        return [[t['atom']]]
    if t['type'] == 'and':
        return to_clauses(t['left'])+to_clauses(t['right'])
    if t['type'] == 'or':
        return [to_clauses(t['left'])[0]+to_clauses(t['right'])[0]]

def clauses_to_dimacs(file,c):
    pass

def contains_or(tree):
    if tree['type'] == "atom":
        return False
    if tree['type'] == 'or':
        return True
    else:
        return contains_or(tree['left']) or  contains_or(tree['right'])

def check_tree(tree,b):
    if tree['type'] == "atom":
        return True
    if tree['type'] == 'and' and b == True:
        return False
    if tree['type'] == "or":
        return check_tree(tree['left'],True) and check_tree(tree['right'],True)
    if tree['type'] == "and":
        return check_tree(tree['left'],b) and check_tree(tree['right'],b)

def print_tree(p,acc):
    if p['type'] == 'atom':
        print(acc+p['type']+":"+str(p['atom']))
    else:
        print(acc+p['type'])
        print_tree(p['left'],acc+"\t")
        print_tree(p['right'],acc+"\t")

#test_table = [0,1,2,3,4,5]
#print_tree(big_and(test_table,lambda x:x),"")
#print_tree(big_or(test_table,lambda x:x),"")

#KO, voir test_tree_2