:- writeln("-- rfmt2.pl --").
:- dynamic fdep/2.
:- dynamic fl/1.


f1(File, Pred) :-
    current_predicate(Pred, Head),
    predicate_property(Head, file(Src)),
    sub_string(Src, _, A, L, '/sdcard/projects/prolog/'),
    sub_string(Src, A, L, _, File).

f3(Fn, L) :-
    findall(Pred, f1(Fn, Pred), L).

f4(Fn, FPl) :-
    concat('/sdcard/projects/prolog/', Fn, S1),
    concat(S1, '.rf', OFn),
    open(OFn, write, OStr),
    with_output_to(OStr, maplist(listing, FPl)),
    close(OStr).

proc_edge(CT, CS, _) :-
    CS=..Tl1,
    CT=..Tl2,
    nth0(2, Tl1, F1),
    nth0(2, Tl2, F2),
    F1=..Tl3,
    F2=..Tl4,
    nth0(0, Tl3, F3),
    nth0(0, Tl4, F4),
    (   fdep(F4, F3)
    ->  true
    ;   F3\==F4
    ->  (   \+ current_op(_, _, F3)
        ->  (   \+ current_op(_, _, F4)
            ->  assertz(fdep(F3, F4))
            ;   true
            )
        ;   true
        )
    ;   true
    ).

mkfdl :-
    retractall(fdep/2),
    retractall(fl/1),
    prolog_walk_code(
                     [ trace_reference(_),
                       on_trace(proc_edge),
                       source(true),
                       verbose(false),
                       module(user)
                     ]),
    findall(F3-F4, fdep(F3, F4), Fl1),
    sort(Fl1, Fl),
    assert(fl(Fl)).

cf1(Co, F1, F2) :-
    fl(Fl),
    nth0(Fi1, Fl, F1),
    nth0(Fi2, Fl, F2),
    compare(Co, Fi1, Fi2),
    !.
cf1(Co, F1, F2) :-
    compare(Co, F1, F2).

rfmt2_2 :-
    writeln('-rfmt2_2'),
    f3(_, FPl1),
    predsort(cf1, FPl1, FPl2),
    f4('all.pl', FPl2).

rfmt2_1 :-
    writeln('-rfmt2_1'),
    forall(f1(Fn, _),
           ( f3(Fn, FPl1),
             predsort(cf1, FPl1, FPl2),
             f4(Fn, FPl2)
           )).

