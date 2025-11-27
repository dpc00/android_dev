:- writeln("-- csbackups.pl --").
:- ensure_loaded(['gb_env.pl', 'funcs.pl']).

getpdir(Si, Dir) :-
    pdir(Si, Pdir),
    sub_string(Pdir, 0, L1, A1, "/sdcard/"),
    sub_string(Pdir, L1, A1, _, Dir),
    !.

chkerr(0, _) :-
    !.
chkerr(Rc, msg) :-
    write(msg),
    writeln(Rc),
    !,
    fail.

csb(Spn, PDir) :-
    write('-csb '),
    netup,
    write(PDir),
    write(->),
    writeln(Spn),
    string_concat("rclone sync /sdcard/", PDir, S1),
    string_concat(S1, " ", S2),
    string_concat(S2, Spn, S3),
    string_concat(S3, ":/", S4),
    string_concat(S4, PDir, S5),
    string_concat(S5, "", S6),
    bash_cmd(S6, Rc),
    !,
    chkerr(Rc, "csb rc: ").

b1_3(Di, Si, SName) :-
    ts2(Di, Si, N2, N1),
    getpdir(Si, Dir1),
    csb(SName, Dir1),
    clr(N2, N1).

b1_1(Di, Si, SName) :-
    (   ts2(Di, Si, N2, N1),
        \+ bctck(N2, N1)
    ;   b1_3(Di, Si, SName)
    ).

csbackup(Di, Si, _, _, _) :-
	writeln('-csbackup'),
	lk(1) ->
		forall(
			member(Svc, Di),
			forall(
				member(Dd, Si),
				(	snm(Svc, SName),
	    			b1_1(Svc, Dd, SName)
	    		)
	    	)
	    ),
		unlk(1)
	;	writeln('lk(1) locked!'), true.
