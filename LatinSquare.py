import math

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
        line_length = nbChiffres*nbChiffres
        x,y = c
        return ((line_length*y)+(nbChiffres)*x)+v
    return f

## Case (x,y) est differente de v
def predicate_isnt(v):
    def f(c): 
        x,y = c
        return -((nbChiffres*y)+(nbChiffres*x)+v)
    return f

#TODOu

## Transformation inverse
def predicate_to_coord(p):
    line_length = (nbChiffres*nbChiffres)
    y = abs(p) // line_length
    x =  (abs(p) % line_length)//nbChiffres
    v = (-((abs(p) % line_length) % nbChiffres),((abs(p)%line_length) % nbChiffres))[p > 0]
    return (x,y,v)

print(predicate_to_coord(predicate_is(4)((4,4))))