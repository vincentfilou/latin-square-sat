import re


def load_clauses(filename):
    spaces = re.compile("\s")
    clauses = []
    file = open(filename,"r")
    buffer = ""
    x = file.read(1)
    while x:
        if buffer == "" and ( x == "p" or x == "c"):
            while True:
                x = file.read(1)
                if x == "\n":
                    x = ""
                    break
        buffer = buffer + x
        if buffer[-2:] == " 0":
            buffer = buffer[0:len(buffer)-2]  
            array = spaces.split(buffer)
            array = [int(x) for x in array if 0< len(x)]
            clauses.append(array)
            buffer = ""
        x = file.read(1)
    return clauses

def get_literals(clauses):
    result = []
    for c in clauses:
        for x in c:
            result.append((x,-x)[x<0])
    return result

def appears(clauses,var):
    for c in clauses:
        if var in c:
            return True
    return False

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

def get_units(clauses):
    return [x[0] for x in clauses if len(x)==1]

def unit_propagation(clauses, unit):
    #print("propagating unit "+str(unit))
    result = clauses[:]
    for c in clauses:
        if unit in c and 1 < len(c):
            result.remove(c)
            #print("removing clause "+str(c))
            continue
        if -unit in c:
            back = c[:]
            result.remove(back)
            back.remove(-unit)
            #print("transforming "+str(c)+" into "+str(back))
            result.append(back)
    return result

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
        #print("========================================")  
        #print(clauses)
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
    #print("========================================")
    #print(clauses)
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
    print("KO")
    return (False,None)
    
    #return DP(clauses)

