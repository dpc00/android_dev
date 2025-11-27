%#!/data/data/com.termux/files/usr/bin/env swipl

:- writeln("-- status.pl --").
:- ensure_loaded(["gb_env.pl", "funcs.pl", "dhash.pl"]).

dirty1(Op, Di, Si, Dd, Sd, Opl) :-
    opdep(Op, Di, Si, Dd, Sd, Opl),
    member(X, Di),
    member(Y, Si),
    ts2(X, Y, N2, N1),
    bctck(N2, N1).

stsupdate(dh(Si, Dh)) :-
    write(" "),
    write(Si),
    srcts(Si, N1),
    rtset(N1),
    !,
    dhset(Si, Dh).

mdp([]) :-
    nl,
    !.
mdp([H|T]) :-
    stsupdate(H),
    mdp(T).

statuses(SDl) :-
    findall(dh(Si, _), src(Si), Pl),
    include(dhck, Pl, SDl).

updatets(N) :-
    (   statuses(Sl),
        write("Status "),
        write(N),
        Sl\=[]
    ->  write(" changed:"),
        mdp(Sl)
    ;   nl
    ).

/*
depchk(T, D) :- dep(T, S1), depchk(S1, D1), D is D1 + 1, !.
depchk(_,0) :- !.

ddepth(D2) :- 
  findall(D1,(dep(T,_), depchk(T,D1)),L),
  print(L),
  max_list(L,D2).

maxd(Op, D2) :- 
  findall(D1, (opdep(Op, T, _, _, _, _), depchk(T,D1)), L),
  max_list(L,D2).

dcmp(<, _, _, D1, D2) :- D1 < D2, write(<).
dcmp(<, E1, E2, D1, D2) :- D1 == D2, E1 @< E2, write(<).
dcmp(=, E1, E2, D1, D2) :- D1 == D2, E1 == E2, write(=).
dcmp(>, E1, E2, D1, D2) :- D1 == D2, E1 @> E2, write(>).
dcmp(>, _, _, D1, D2) :- D1 > D2, write(>).

opcmp(Delta, E1, E2) :-  maxd(E1,D1), maxd(E2,D2), dcmp(Delta, E1, E2, D1, D2).

oplst(L2) :- 
  findall(Op,dirty1(Op, _, _, _, _, _),L1),
  write(L1), nl,
  predsort(opcmp,L1,L2),
  write(L2), nl,!.
*/
