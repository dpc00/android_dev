:- writeln("-- gitbackup.pl --").
:- ensure_loaded(["gb_env.pl","funcs.pl","git.pl","netup.pl"]).

gud3(Wt, Rmt) :-
    getRevs(Wt, Rl, Rmt),
    (   Rl\=[]
    ->  doPush(Wt, Rl, Rmt)
    ;   true
    ).

gud2(Wt) :-
    (   git_diff2(Wt)
    ->  getCommits(Wt, Cl),
        doCommit(Wt, Cl)
    ;   true
    ).

gud1(Wt) :-
    (   git_diff1(Wt)
    ->  getAdds(Wt, Al),
        doAdds(Wt, Al)
    ;   true
    ).

gud(Wt, Rmt) :-
    gud1(Wt),
    gud2(Wt),
    gud3(Wt, Rmt).

gitbackup(Di, Si, _, _, Opt) :-
	writeln('-gitbackup'),
    member(wt(Wt), Opt),
    (   member(add(true), Opt)
    ->  gud1(Wt)
    ;   true
    ),
    (   member(commit(true), Opt)
    ->  gud2(Wt)
    ;   true
    ),
    (   member(push(true), Opt)
    ->  (   member(rmt(Rmt), Opt),
        	gud3(Wt, Rmt),
        	member(S, Si),
            dhset(S)
        )
    ;   true
    ),
    forall(
    	member(T, Di),
    	forall(
    		member(S, Si),
    		(	ts2(T, S, N2, N1),
				clr(N2, N1)
			;	true
			)
		)
	).
