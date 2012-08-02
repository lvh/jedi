# goto command test are a different in syntax

a = 1

#! []
b
#! ['a=1']
a

b = a
c = b
#! ['c=b']
c

#! ['module math']
import math
#! ['import math']
math

#! ['import math']
b = math
#! ['b=math']
b

class C(object):
    def b(self):
        #! ['b=math']
        b
        #! ['def b']
        self.b
        #! 14 ['def b']
        self.b()
        #! 11 ['class C']
        self.b
        return 1

    #! ['def b']
    b

#! ['b=math']
b

#! ['def b']
C.b
#! ['def b']
C().b
#! 0 ['class C']
C().b
#! 0 ['class C']
C().b

D = C
#! ['def b']
D.b
#! ['def b']
D().b

#! 0 ['D=C']
D().b
#! 0 ['D=C']
D().b

def c():
    return ''

#! ['def c']
c
#! 0 ['def c']
c()

# -----------------
# imports
# -----------------

#! ['module import_tree']
import import_tree

#! ['module mod1']
import import_tree.mod1

#! ['module mod1']
import import_tree.pkg.mod1

#! ['module mod1']
from import_tree import mod1

