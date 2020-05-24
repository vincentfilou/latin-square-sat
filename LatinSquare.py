import math
import Propositions

nbChiffres = 2

def Product(a,b):
    product = []
    for x in a:
        for y in b:
            product.append((x,y))
    return product

## La colonne x
def column(x):
    return Product([x],range(0,nbChiffres))

## La ligne y
def line(y):
    return Product(range(0,nbChiffres),[y])


# Predicats de base

## Case (x,y) est egale a v
def predicate_is(v):
    def f(c): 
        line_length = nbChiffres*(nbChiffres+1)
        x,y = c
        return ((line_length*y)+(nbChiffres+1)*x)+v
    return f

## Case (x,y) est differente de v
def predicate_isnt(v):
    def f(c): 
        line_length = nbChiffres*(nbChiffres+1)
        x,y = c
        return -(((line_length*y)+(nbChiffres+1)*x)+v)
    return f

#TODOu

## Transformation inverse
def predicate_to_coord(p):
    line_length = (nbChiffres*(nbChiffres+1))
    y = abs(p) // line_length
    x =  (abs(p) % line_length)//(nbChiffres+1)
    v = (-((abs(p) % line_length) % (nbChiffres+1)),((abs(p)%line_length) % (nbChiffres+1)))[p > 0]
    return (x,y,v)

def exists_line(x):
    return Propositions.big_and(range(1,nbChiffres), lambda v:Propositions.big_or(line(x),lambda c:Propositions.build_atom(predicate_is(v)(c))))

def exists_column(y):
    return Propositions.big_and(range(1,nbChiffres+1), lambda v:Propositions.big_or(column(y),lambda c:Propositions.build_atom(predicate_is(v)(c))))

#NOK multiple copies of subtree

def one_per_line_inner(c):
    x,y = c
    l = line(y)
    l.remove(c)
    return Propositions.big_and(range(1,nbChiffres+1), lambda v:Propositions.build_or(Propositions.build_atom(predicate_isnt(v)(c)), Propositions.big_and(l, lambda c0:Propositions.build_atom(predicate_isnt(v)(c0)))))


def one_per_line(y):
    return Propositions.big_and(line(y), one_per_line_inner)

def one_per_column(y):
    pass

def one_per_coord(c):
    pass

print(predicate_to_coord(predicate_isnt(2)((1,1))))
#Propositions.print_tree(exists_line(1),"")
Propositions.print_tree(exists_column(1),"")
Propositions.print_tree(one_per_line(0),"")