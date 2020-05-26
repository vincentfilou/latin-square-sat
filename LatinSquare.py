import Propositions
import Clauses

problemeSize = 2

def Product(a,b):
    product = []
    for x in a:
        for y in b:
            product.append((x,y))
    return product

## La colonne x
def column(x):
    return Product([x],range(0,problemeSize))

## La ligne y
def line(y):
    return Product(range(0,problemeSize),[y])


# Predicats de base

## Case (x,y) est egale a v
def predicate_is(v):
    def f(c): 
        line_length = problemeSize*(problemeSize+1)
        x,y = c
        return ((line_length*y)+(problemeSize+1)*x)+v
    return f

## Case (x,y) est differente de v
def predicate_isnt(v):
    def f(c): 
        line_length = problemeSize*(problemeSize+1)
        x,y = c
        return -(((line_length*y)+(problemeSize+1)*x)+v)
    return f


## Transformation inverse
def predicate_to_coord(p):
    line_length = (problemeSize*(problemeSize+1))
    y = abs(p) // line_length
    x =  (abs(p) % line_length)//(problemeSize+1)
    v = (-((abs(p) % line_length) % (problemeSize+1)),((abs(p)%line_length) % (problemeSize+1)))[p > 0]
    return (x,y,v)

def exists_line_(x):
    return Propositions.big_and(range(1,problemeSize), lambda v:Propositions.big_or(line(x),lambda c:Propositions.build_atom(predicate_is(v)(c))))

def exists_line():
    return Propositions.big_and(range(0,problemeSize), exists_line_)

def exists_column_(y):
    return Propositions.big_and(range(1,problemeSize+1), lambda v:Propositions.big_or(column(y),lambda c:Propositions.build_atom(predicate_is(v)(c))))

def exists_column():
    return Propositions.big_and(range(0,problemeSize), exists_column_)

def one_per_line_inner(c):
    x,y = c
    l = line(y)
    l.remove(c)
    return Propositions.big_and(range(1,problemeSize+1), lambda v:Propositions.build_or(Propositions.build_atom(predicate_isnt(v)(c)), Propositions.big_and(l, lambda c0:Propositions.build_atom(predicate_isnt(v)(c0)))))

def one_per_line_(y):
    return Propositions.big_and(line(y), one_per_line_inner)


def one_per_line():
    return Propositions.big_and(range(0,problemeSize),one_per_line_)

def one_per_column_inner(c):
    x,y = c
    l = column(x)
    l.remove(c)
    return Propositions.big_and(range(1,problemeSize+1), lambda v:Propositions.build_or(Propositions.build_atom(predicate_isnt(v)(c)), Propositions.big_and(l, lambda c0:Propositions.build_atom(predicate_isnt(v)(c0)))))


def one_per_column_(x):
    return Propositions.big_and(column(x), one_per_column_inner)

def one_per_column():
    return Propositions.big_and(range(0,problemeSize),one_per_column_)

def one_per_file_inner(c):
    def f(v):
        vs = [x for x in range(1,problemeSize+1)]
        vs.remove(v)
        return Propositions.build_or(Propositions.build_atom(predicate_isnt(v)(c)),Propositions.big_and(vs, lambda v0: Propositions.build_atom(predicate_isnt(v0)(c))))
    return f

def one_per_file():
    return Propositions.big_and(Product(range(0,problemeSize),range(0,problemeSize)),lambda c:Propositions.big_and(range(1,problemeSize+1),one_per_file_inner(c)))


def print_result(r):
    acc = ""
    for y in range(0,problemeSize):
        for x in range(0,problemeSize):
            for c in r:
                (a,b,v) = c
                if a == x and b == y:
                    acc+=str(v)+" "
        acc += "\n"
    print(acc)      

exists = Propositions.build_and(exists_line(),exists_column())
tree = Propositions.build_and(one_per_column(), Propositions.build_and(one_per_line(),Propositions.build_and(one_per_file(),exists)))
normalized_tree = Propositions.normalize(tree)
clauses = Propositions.to_clauses(normalized_tree)
solved,values = Clauses.DP(clauses)

result = set()

if solved == True:
    for c in values:
        if 0 < c[0]:
            result.add(predicate_to_coord(c[0]))
    print_result(result)
else:
    print("Unsolvable")