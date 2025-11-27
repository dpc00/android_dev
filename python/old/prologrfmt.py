from datetime import datetime
from pyswip import Prolog, Functor, Atom, Variable, Query, Term, registerForeign, getList, putList, putTerm
from toposort import topological_sort

pl = Prolog()

pl.consult("/sdcard/projects/prolog/main.pl")
mkfdl = Functor('mkfdl', 0)
fl = Functor('fl', 1)
retract = Functor('retract', 1)
assertf = Functor('assert', 1)
rfmt2_1 = Functor('rfmt2_1', 0)
rfmt2_2 = Functor('rfmt2_2', 0)

Fl = Variable()

q1 = Query(mkfdl, fl(Fl))

if q1.nextSolution():
    print(type(Fl))
    print(type(Fl.value))
    l = Fl.value
    bl = []
    for li in l:
        # print(type(li), end=' ')
        if isinstance(li, Functor):
            caller = li.args[0].value
            # print(caller, end=' ')
            callee = li.args[1].value
            # print(callee)
            bl.append([caller, callee])
    # print(bl)
    q1.closeQuery()
    p1 = topological_sort(bl)
    print(p1)
    p1 = [t for elem in p1 for t in elem]
    print(len(p1))
    t1 = Term()
    putList(t1.handle, [n for n in p1])
    q2 = Query(retract(fl(Fl)), assertf(fl(t1)))
    if q2.nextSolution():
        pass
    q2.closeQuery()
    q3 = Query(rfmt2_1())
    if q3.nextSolution():
        pass
    q3.closeQuery()
    q4 = Query(rfmt2_2())
    if q4.nextSolution():
        pass
    q4.closeQuery()
