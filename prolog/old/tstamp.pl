:- writeln("-- tstamp.pl --"). 
:- ensure_loaded(["gb_env.pl","funcs.pl"]).
:- dynamic tsd/1.

tsd(D) :- D = _{},
   retractall(tsd(_)),
   assert(tsd(D)).

ts2(T, S, N2, N1) :-
    dstts(T, S, N2),
    srcts(S, N1).

prefn(Pre, N, Tsfn) :-
    pre(Pre, S1),
    string_concat(S1, N, Tsfn).

tsmakeexist(Fn) :-
    (   exists_file(Fn)
    ->  true
    ;   open(Fn, write, Str),
        close(Str)
    ).

savets :-
    pre('FLAGS', S1),
    string_concat(S1, "/tsd.pl", S2),
    open(S2, write, St1),
    tsd(D1),
    write_term(St1, tsd(D1), [fullstop(true), nl(true), quoted(true)]),
    close(St1).

tstime_m(Pre, N, Ft) :-
    tsd(D1),
    (   var(Ft)
    ->  catch(( ( '.'(D1, Pre, A),
                  '.'(A, N, B)
                ),
                Ft=B
              ),
              error(_, _),
              ( get_time(Ft),
                tstime_m(Pre, N, Ft)
              ))
    ;   retract(tsd(D1)),
        '.'(D1, put(Pre/N, Ft), C),
        D2=C,
        assert(tsd(D2)),
        savets
    ).

rtset :-
    findall(N1, (srcts(_, N1), rtset(N1)), _),
    savets.

rtset(N) :-
    get_time(Ct),
    tstime_m(rtbk, N, Ct).

rtset(N, Mt) :-
    tstime_m(rtbk, N, Mt).

bctck(N2, N1) :-
    tstime_m(rtbk, N1, Ft1),
    tstime_m(ct, N2, Ft2),
    Ft1>Ft2.

loadts :-
    pre('FLAGS', S1),
    string_concat(S1, "/tsd.pl", S2),
    (   exists_file(S2)
    ->  open(S2, read, St1),
        read_term(St1, tsd(D1), []),
        retractall(tsd(_)),
        assert(tsd(D1)),
        close(St1)
    ;   true
    ).

clr(N2, N1) :-
    tstime_m(rtbk, N1, Ft1),
    tstime_m(ct, N2, Ft2),
    (   Ft1=\=Ft2
    ->  tstime_m(ct, N2, Ft1),
        write("-clr"),
        writev(N2, 'N2'),
        writev(N1, 'N1'),
        dstts(T, S, N2),
        srcts(S, N1),
        writev(T, 'T'),
        writev(S, 'S'),
        nl
    ;   true
    ),
    nl.

bctclr(N2, N1) :-
    tstime_m(rtbk, N1, Ft1),
    tstime_m(ct, N2, Ft1),
    write("-bctclr"),
    writev(N2, 'N2'),
    writev(N1, 'N1'),
    nl.

:- loadts.
