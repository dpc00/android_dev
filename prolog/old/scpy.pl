%#!/data/data/com.termux/files/usr/bin/env swipl
:- writeln("-- scpy.pl --").

:- ensure_loaded(
  ["gb_env.pl",
  "funcs.pl"]).

noop(Di, Si, _, _, _) :-
    test_ts2(Di, Si, N2, N1),
    clr(N2, N1).

scpy([Di], [Si], [Dd], [Sd], Opt) :-
    ts2(Di, Si, N2, N1),
    (   bctck(N2, N1)
    ->  member(files(Fl), Opt),
        (   member(exec(true), Opt)
        ->  forall(member(Ex, Fl), fcx(Dd, Sd, Ex))
        ;   forall(member(Ex, Fl), fc(Dd, Sd, Ex))
        ),
        clr(N2, N1),
        (   Si==rclone_as_src
        ->  dhset(Si)
        ;   true
        )
    ;   true
    ).

