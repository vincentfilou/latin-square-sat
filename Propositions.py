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
        return build_atom(f(t[0]))
    else:
        return build_and(big_and(t[0:1],f),big_and(t[1:],f))

def big_or(t,f):
    if len(t) == 1:
        return build_atom(f(t[0]))
    else:
        return build_or(big_or(t[0:1],f),big_or(t[1:],f))

def proposition_to_dimacs(p):
    pass

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

# test_tree = build_or(build_and(build_atom(1), build_and(build_atom(2),build_atom(3))),build_and(build_atom(4),build_and(build_atom(5),build_atom(6))))
# test_tree_2 = build_or(build_and(build_atom(1),build_atom(2)),build_and(build_or(build_atom(3),build_atom(3)),build_atom(4)))
# print_tree(normalize(test_tree_2),"")