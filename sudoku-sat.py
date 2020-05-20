
# Ensembles manipules

## Produit cartesien
def Product(a,b):
    product = []
    for x in a:
        for y in b:
            product.append((x,y))
    return product

## La colonne x
def column(x):
    return Product([x],range(0,9))

## La ligne y
def line(y):
    return Product(range(0,9),[y])

## Le carre x,y
def square(x,y):
    return Product(range(x*3,x*3+3), range(y*3,y*3+3))


# Predicats de base

## Case (x,y) est egale a v
def predicate_is(v):
    def f(x,y): 
        return (90*y)+(10*x)+v
    return f

## Case (x,y) est differente de v
def predicate_isnt(v):
    def f(x,y): 
        return -((90*y)+(10*x)+v)
    return f

## Transformation inverse
def predicate_to_coord(p):
    y = abs(p) // 90
    x =  (abs(p) % 90)//10
    v = (-((abs(p) % 90) % 10),((abs(p)%90)%10))[p > 0]
    return (x,y,v)

print(predicate_isnt(1)(0,1))

# print(predicate_to_coord(predicate_isnt(9)(1,8)))