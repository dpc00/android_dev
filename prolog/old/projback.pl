:- writeln("-- projback.pl --").
:- ensure_loaded(["gb_env.pl","funcs.pl"]).

mkzip(Di, Si, [Dd], [Sd], Opt) :-
    member(zipfile(Zf), Opt),
    tdir(Dd, O1),
    string_concat(O1, "/", O2),
    string_concat(O2, Zf, O3),
    string_concat("zip -r -q ", O3, C1),
    string_concat(C1, " ", C2),
    pdir(Sd, I1),
    string_concat(I1, "/*", I2),
    string_concat(C2, I2, C3),
    writeln(C3),
    srun(C3, Rc),
    (   Rc=\=0
    ->  write("zip rc: "),
        writeln(Rc),
        fail
    ;   forall(
			member(T, Di),
			forall(
				member(S, Si),
               ( ts2(T, S, N4, N3),
                 clr(N4, N3)
               )
            )
        )
    ).

