:- writeln("-- opts.pl --").
:- ensure_loaded(["gb_env.pl","funcs.pl","tstamp.pl","dhash.pl","status.pl"]).

:- dynamic pass/1.

:- retractall(pass/1).
:- dynamic gt/2.

incp(P1) :-
    (   pass(P1)
    ->  retract(pass(P1)),
        P2 is P1+1,
        assert(pass(P2))
    ;   P1 is 1,
        assert(pass(P1))
    ).

clean :-
    \+ dirty1(_, _, _, _, _, _).

nodeps(T) :-
	writeln('-nodeps'),
    \+ dep(_, T).

dag(G1) :-
	writeln('-dag'),
    findall(Sa-Ta, dep(Ta, Sa), Egs),
    add_edges([], Egs, G1).

nts(G) :-
	writeln('-nts'),
    dag(G1),
    top_sort(G1, G).

dagt(G2) :-
	writeln('-dagt'),
    dag(G1),
    transpose_ugraph(G1, G2).

gproc3((T, Opl, Res)) :-
	write('-gproc3 '),
	writeln(T),
    Op=..Opl,
    (   call(Op)
    ->  Res=true,
        incp(P1),
        updatets(P1)
    ;   Res=false
    ).

gproc2(T) :-
	writeln('-gproc2'),
    findall([Op, Tl, Si, Dd, Sd, Opt],
            (	dirty1(Op, Tl, Si, Dd, Sd, Opt),
            	member(T, Tl)
            ),
            L1),
    (   L1==[]
    ->  true
    ;   sort(L1, L2),
        findall((T, X, _), member(X, L2), L3),
        maplist(gproc3, L3),
        \+ member((T, _, false), L3)
    ).

gproc([]) :-
    writeln('-gproc[]').
gproc([T|Tl]) :-
	writeln('-gproc'),
    gproc2(T),
    gproc(Tl).

opexec :-
	writeln('-opexec'),
    retractall(pass/1),
    nts(G1),
    !,
    writeln(G1),
    incp(P1),
    updatets(P1),
    (   gproc(G1)
    ->  (   clean
        ->  halt(0)
        ;   fail
        )
    ;   halt(1)
    ).

