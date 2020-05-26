# l'ensemble des litéraux (atomes) d'une formule
def get_literals(clauses):
    result = []
    for c in clauses:
        for x in c:
            result.append((x,-x)[x<0])
    return result

# un littéral apparait'il dans l'ensemble des clauses?
def appears(clauses,var):
    for c in clauses:
        if var in c:
            return True
    return False

# Ensemble des litteraux apparaissant uniquement en positif (A) ou en négatif (Non A)
def get_pure_literals(clauses):
    result = []
    for c in clauses:
        for x in c:
            if not(appears(clauses,-x)) and not (x in get_units(clauses)):
                result.append(x)
    return result

def pure_elim(clauses,pure):
    result = clauses[:]
    for c in clauses:
        if pure in c:
            result.remove(c)
    return result

# Ensemble des litteraux donc la valeur est connue (une clause contient un unique literal (ex: Non A))
# Comme la liste des clauses représente une conjonction, ce litteral est Vrai
def get_units(clauses):
    return [x[0] for x in clauses if len(x)==1]

# Si un literal est vrai, toute les clauses le contenant sont vrai.
# De même sa négation est fausse et peut être supprimé de toute les clauses.
def unit_propagation(clauses, unit):
    result = clauses[:]
    for c in clauses:
        if unit in c and 1 < len(c):
            result.remove(c)
            continue
        if -unit in c:
            back = c[:]
            result.remove(back)
            back.remove(-unit)
            result.append(back)
    return result

# La formule est elle une solution? 
# i.e. une formule ne contient que des litteraux, et pas de contradictions (clauses non vides)
def is_sat(clauses):
    if len(clauses) == 0:
        return False
    for c in clauses:
        if 0 == len(c):
            return False
        if 1 < len(c):
            return False
    return True

def is_unsat(clauses):
    for c in clauses:
        if 0 == len(c):
            return True
    return False


def DP(clauses):
    x = []
    while x != clauses:
        x = clauses[:]
        units = get_units(clauses)
        for unit in units:
            clauses = unit_propagation(clauses,unit)
        lits = get_pure_literals(clauses)
        for lit in lits:
            clauses = pure_elim(clauses,lit)
            clauses = clauses +[[lit]]
        if(is_unsat(clauses)):
            return(False,None)
    if is_sat(clauses):
        return (True,clauses)
    if is_unsat(clauses):
        return (False,None)
    lits = get_literals(clauses)
    units = get_units(clauses)
    lits = [y for y in lits if not(y  in units)]
    if 0< len(lits):
        (sat0,pos0) = DP(clauses+[[lits[0]]])
        if sat0:
            return (True,pos0)
        (sat1,pos1)= DP(clauses+[[-(lits[0])]])
        if sat1:
            return (True,pos1)
    return (False,None)

