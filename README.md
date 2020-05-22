# Traduit un sudoku en formule cnf pour etre resolu par un sat solver.

## Format, coordonnées et variables booléennes

## KO, 10 -> 0

```
case 0,0: vars 0 1 2 3 4 5 6 7 8 9; case 0,1: 10 11 12 13 14 15 16 17 18 19,
case 0,2: (90*0)+(10*2)+1... 2*10 + 9 case 0,8: 
case 1,x: (90*1)+(10*x)+(1..9), ..., (90*1)+(10*8)+(1..9)
case 2,x: (90*2)+(10*x)+(1..9)
```

```
case 0,0 = 3 -> 3
case 0,1 = 3 -> 12
case 0,1 /= 3 -> -12
```

Attention! On suppose ici que x /: range(0,x) i.e. range(0,x) = [0,1,...,x-1]

```
column(x)  = [(x,0),(x,1),...,(x,8)]
           = Product([x],range(0,9))
line(y)    = [(0,y),(1,y),..,(8,y)]
           = Product(range(0,9),[y])
carre(x,y) = [ (x*3,y*3+0),(x*3,y*3+1),(x,y*3+2),(x*3+1,y*3),... ]
	   = Product(range(x*3,x*3+3), range(y*3,y*3+3))
```

## Calcul de la formule

### Predicats de base

```
is    (x,y,v) =   ((81*y)+(9*x)+v)
isNot (x,y,v) = - ((81*y)+(9*x)+v)
```

### fonctions BigOr et BigAnd

voir Propositions

### Exclusion:

#### TODO: Appliquer big_and au produit, puis recursivement a range(1,10), etc

```
Pour tout x,y in Product(range(0,9), range(0,9)):
   Pour tout i in range(1,10) :
      isNot(x,y,i) or
         ( (BigAnd column(x)\{(x,y)},      fun a,b => isNot(a,b,i)) and
           (BigAnd line(y)\{(x,y)},        fun a,b => isNot(a,b,i)) and
           (BigAnd carre(x/3,y/3)\{(x,y)}, fun a,b => isNot(a,b,i)) )
```

### Presence:

```
Pour tout i in range(1,10) :
   Pour tout x,y in [(0,0),(0,1),(0,2),...,(2,0),(2,1),(2,2)] :
      BigOr carre(x,y), fun a,b => is(a,b,i)
   and
   Pour tout y in [0..8] :
      BigOr ligne(y),   fun a,b => is(a,b,i)
   and 
   Pour tout x in [0..8] :
      BigOr colonne(x), fun a,b => is(a,b,i) 
```

### Un chiffre par case
pour tout i in range(1,10):
   pour tout c in Product(range(0,9), range(0,9))
      predicate_isnt(i)(c) or BigAnd(range(0,10).remove(i), predicate_isnt(i)(c)) 

## Passage de la formule resultante en CNF

voir Propositions/normalize
