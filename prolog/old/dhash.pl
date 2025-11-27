:- writeln("-- dhash.pl --").
:- ensure_loaded(['gb_env.pl', 'funcs.pl']).

pre(dh, X) :-
    pre('FLAGS', X1),
    string_concat(X1, "/.dh", X).

:- (dynamic using_db2/0).
:- (dynamic dhd/1).

dhd(D) :- D = _{},
   retractall(dhd(_)),
   assert(dhd(D)).
   
dircmd("ls -AgGlR --block-size=1 --time-style=+%s --color=never ").

savedh :-
    pre('FLAGS', S1),
    string_concat(S1, "/dhd.pl", S2),
    open(S2, write, St1),
    dhd(D1),
    write_term(St1, dhd(D1), [fullstop(true), nl(true), quoted(true)]),
    close(St1).

loaddh :-
    pre('FLAGS', S1),
    string_concat(S1, "/dhd.pl", S2),
    loaddh(S2).

loaddh(S1) :-
    \+ exists_file(S1),
    !.
loaddh(S2) :-
    open(S2, read, St1),
    read_term(St1, dhd(D1), []),
    retractall(dhd(_)),
    assert(dhd(D1)),
    close(St1).

dhstrf_m(Si, Dh) :-
    dhd(D1),
    var(Dh),
    !,
    catch(( '.'(D1, Si, A),
            Dh=A
          ),
          error(_, _),
          Dh="nohashyet").
dhstrf_m(Si, Dh) :-
    dhd(D1),
    nonvar(Dh),
    !,
    '.'(D1, put(Si, Dh), A),
    D2=A,
    retract(dhd(D1)),
    assert(dhd(D2)).

sha256sumd(Dir, Sum) :-
    dircmd(Dc),
    string_concat(Dc, Dir, Cmd),
    bash_cmd_out(Cmd, S1, Rc),
    (   Rc==0
    ->  sha_hash(S1, SumC, [algorithm(sha256)]),
        hash_atom(SumC, SumH),
        atom_string(SumH, Sum)
    ).

onedh(Si2, Dh) :-
    pdir(Si2, Dir),
    sha256sumd(Dir, Dh).

dhstrd([H|T], CDh) :-
    !,
    findall(Dh,
		(	member(Si2, [H|T]),
			onedh(Si2, Dh)
		),
		LDh
	),
    foldl(string_concat, LDh, "", Cs),
    sha_hash(Cs, CDhC, [algorithm(sha256)]),
    hash_atom(CDhC, CDhA),
    atom_string(CDhA, CDh).
dhstrd(Si, CDh) :-
    onedh(Si, CDh).

dhset(Si) :-
    dhstrd(Si, Dh),
    dhstrf_m(Si, Dh),
    savedh.

dhset(Si, Dh) :-
    dhstrf_m(Si, Dh),
    savedh.

dhck(dh(Si, Dh2)) :-
    nonvar(Si),
    var(Dh2),
    dhstrf_m(Si, Dh1),
    dhstrd(Si, Dh2),
    Dh1\==Dh2.


:- loaddh, assert(using_db2).
