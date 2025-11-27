:- writeln("-- fcutils.pl --").
:- ensure_loaded(['gb_env.pl', 'funcs.pl']).

fex(Fn) :-
    member(Fn, ['.', ..]).

nodots(Fl1, Fl2) :-
    exclude(fex, Fl1, Fl2).

files(Fl) :-
    pdir(pro, PDir),
    string_concat(PDir, "/*.pl", PSpec),
    expand_file_name(PSpec, Fl).

files(Si, Ex, Fl) :-
    pdir(Si, Sd1),
    string_concat(Sd1, "/", Sd2),
    string_concat(Sd2, Ex, Sd3),
    expand_file_name(Sd3, Fl).

file(Si, Ex, Fn) :-
    files(Si, Ex, Fl),
    member(Fn, Fl).

sha256sums(S1, Sum) :-
    string(S1),
    sha_hash(S1, SumC, [algorithm(sha256)]),
    hash_atom(SumC, SumH),
    atom_string(SumH, Sum).

sha256sumf(Fn, Sum) :-
    exists_file(Fn), !,
    open(Fn, read, P1, [type(binary)]),
    read_string(P1, _, S1),
    close(P1),
    sha256sums(S1, Sum).
sha256sumf(_, "None").

time_file3(IFs, FFt) :-
    maxFt2(IFs, FFt),
    !.
time_file3(_, 0).

maxFt2(Ds1, Mt) :-
    directory_files(Ds1, Fl1),
    nodots(Fl1, Fl2),
    maplist(directory_file_path(Ds1), Fl2, Fl3),
    maplist(time_file2, Fl3, Tl),
    max_list(Tl, Mt).

time_file2(IFs, OFt) :-
    exists_file(IFs),
    !,
    time_file(IFs, OFt).
time_file2(IFs, OFt) :-
    exists_directory(IFs),
    !,
    time_file(IFs, Dt),
    time_file3(IFs, FFt),
    OFt is max(Dt, FFt).

maxFt(Fs1, Mt) :-
    time_file2(Fs1, Mt).

fdiff(Fn1, _) :-
	\+ exists_file(Fn1),
    !, fail.
fdiff(Fn1, Fn2) :-
	exists_file(Fn1),
    \+ exists_file(Fn2),
    !.
fdiff(Fn1, Fn2) :-
	exists_file(Fn1),
	exists_file(Fn2),
	time_file(Fn1, Ft1),
	time_file(Fn2, Ft2),
	Ft1 > Ft2,
	!.
fdiff(Fn1, Fn2) :-
	exists_file(Fn1),
	exists_file(Fn2),
	size_file(Fn1, Fs1),
	size_file(Fn2, Fs2),
	Fs1 \== Fs2,
	!.
fdiff(Fn1, Fn2) :-
    exists_file(Fn1),
	exists_file(Fn2),
	sha256sumf(Fn1, Fh1),
    sha256sumf(Fn2, Fh2),
    Fh1\==Fh2,
	!.

check_directory(Dd) :-
    exists_directory(Dd),
    !.
check_directory(Dd) :-
    make_directory_path(Dd).

sdn(Ti, Si, Ex, Fn1, Fn2) :-
    pdir(Si, Sd),
    tdir(Ti, Dd),
    !,
    file(Si, Ex, Fn1),
    sub_string(Fn1, 0, L, A, Sd),
    sub_string(Fn1, L, A, 0, Bfn),
    string_concat(Dd, Bfn, Fn2),
	file_directory_name(Fn2, FDd),
	check_directory(FDd).

fcx(Ti, Si, Ex) :-
    forall(sdn(Ti, Si, Ex, Fn1, Fn2),
           (   fdiff(Fn1, Fn2)
           ->  write("copy "),
               write(Fn1),
               write("->"),
               write(Fn2),
               nl,
               copy_file(Fn1, Fn2),
               chmod(Fn2, 496),
               time_file(Fn1, Ft1),
               set_time_file(Fn2, [], [modified(Ft1)])
           ;   true
           )).

fc(Ti, Si, Ex) :-
    forall(sdn(Ti, Si, Ex, Fn1, Fn2),
           (   fdiff(Fn1, Fn2)
           ->  write("copy "),
               write(Fn1),
               write("->"),
               write(Fn2),
               nl,
               copy_file(Fn1, Fn2),
               time_file(Fn1, Ft1),
               set_time_file(Fn2, [], [modified(Ft1)])
           ;   true
           )).


