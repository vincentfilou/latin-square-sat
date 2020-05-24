import Propositions
import Clauses
# Ensembles manipules

## Produit cartesien
def Product(a,b):
    product = []
    for x in a:
        for y in b:
            product.append((x,y))
    return product




# Predicats de base

## Case (x,y) est egale a v
def predicate_is(v):
    def f(c): 
        x,y = c
        return (90*y)+(10*x)+v
    return f

## Case (x,y) est differente de v
def predicate_isnt(v):
    def f(c): 
        x,y = c
        return -((90*y)+(10*x)+v)
    return f

## Transformation inverse
def predicate_to_coord(p):
    y = abs(p) // 90
    x =  (abs(p) % 90)//10
    v = (-((abs(p) % 90) % 10),((abs(p)%90)%10))[p > 0]
    return (x,y,v)

def excl(i):
    def excl2(k):
        return Propositions.build_atom(predicate_isnt(i)(k))
    return excl2


def exclusion_i(x,y):
    def f(i):
        col = column(x)
        li = line(y)
        sq = square(x//3,y//3)
        col.remove((x,y))
        li.remove((x,y))
        sq.remove((x,y))

        exclusion_column = Propositions.big_and(col, excl(i))
        exclusion_line = Propositions.big_and(li, excl(i))
        exclusion_square = Propositions.big_and(sq, excl(i))
        is_not = Propositions.build_atom(predicate_isnt(i)((x,y)))
        return (Propositions.build_or(is_not,Propositions.build_and( exclusion_column , Propositions.build_and(exclusion_line, exclusion_square))))
    return f

def exclusion_coord(p):
    x,y = p
    return Propositions.big_and(range(1,10),exclusion_i(x,y))


def exclusion():
    return Propositions.big_and(Product(range(0,9),range(0,9)), exclusion_coord)


#KO: predicate_is takes 3 args

def presence_fun(i):
    squares = Product(range(0,2), range(0,2))
    lines = range(0,8)
    columns = range(0,8)
    def square_presence(c):
        x,y = c
        return Propositions.big_or(square(x,y),lambda c:Propositions.build_atom(predicate_is(i)(c)))

    def line_presence(y):
        return Propositions.big_or(line(y),lambda c:Propositions.build_atom(predicate_is(i)(c)))

    def column_presence(x):
        return Propositions.big_or(column(x),lambda c:Propositions.build_atom(predicate_is(i)(c)))

    sq_pres = Propositions.big_and(squares,square_presence)
    ln_pres = Propositions.big_and(lines,line_presence)
    cl_pres =  Propositions.big_and(columns,column_presence)
    return Propositions.build_and(sq_pres,Propositions.build_and(ln_pres,cl_pres))

def presence():
    return Propositions.big_and(range(1,10),presence_fun)

def all_but_this_(c):
    def all_but_this_in(i):
        isnt_i = Propositions.build_atom(predicate_isnt(i)(c))
        to_exclude = [0,1,2,3,4,5,6,7,8,9]
        to_exclude.remove(i)
        not_others = Propositions.big_and(to_exclude, (lambda x:Propositions.build_atom(predicate_isnt(x)(c))))
        return Propositions.build_or(isnt_i, not_others)
    return all_but_this_in

def all_but_this(c):
    excl = Propositions.big_and(range(0,10),all_but_this_(c))
    return excl


def one_digit():
    return Propositions.big_and(Product(range(0,9), range(0,9)),all_but_this)

tree = Propositions.build_and(presence(),exclusion())
tree1 = Propositions.build_and(tree, one_digit())
normalized_tree = Propositions.normalize(tree1)
print(Propositions.check_tree(normalized_tree, False))
clauses = Propositions.to_clauses(normalized_tree)
clauses = clauses +[[predicate_is(1)((0,0))]]
print(Clauses.DP(clauses))
#Propositions.clauses_to_dimacs("test.txt", clauses)