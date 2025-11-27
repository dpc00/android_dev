:- writeln("-- funcs.pl --").
:- ensure_loaded(['gb_env.pl']).

pre('bkx', X) :- pre('FLAGS', X1), string_concat(X1, "/.bkx", X).

unlk(N) :-
    pre(bkx, X1),
    number_string(N, S1),
    string_concat(X1, S1, Dir),
    exists_directory(Dir),
    delete_directory(Dir).

lk(N) :-
    pre(bkx, X1),
    number_string(N, S1),
    string_concat(X1, S1, Dir),
    \+ exists_directory(Dir),
    make_directory(Dir).

bcm(Fname, Cmd) :-
    write("-"),
    write(Fname),
    write(" "),
    write(Cmd),
    nl.

cmp1(S1, N1, S2, S3, N2) :-
    (   bctck(N2, N1)
    ->  write(S1),
        write(" rtbk"),
        write(N1),
        write(", "),
        write(S2),
        write(" "),
        write(S3),
        write(" ct"),
        writeln(N2)
    ;   true
    ).

writev(T, _) :-
    nonvar(T),
    !,
    write(" "),
    write(T).
writev(T, Nm) :-
    var(T),
    !,
    write(" _"),
    write(Nm).

btest :-
    write("-btest"),
    nl,
    forall(dep(T, S),
           ( ts2(T, S, N2, N1),
             cmp1(S, N1, T, S, N2)
           )).

bset :-
    write("-bset"),
    nl,
    forall(dep(T, S),
           ( ts2(T, S, N2, N1),
             get_time(Now),
             tstime_m(rtbk, N2, Now),
             tstime_m(ct, N1, 0)
           )),
    savets.

srun(Cmd, Rc) :-
    *bcm("srun", Cmd),
    catch(( process_create(path(bash), ["-c", Cmd], []),
            Rc=0
          ),
          error(E, _),
          (   process_error(_, exit(Rc))=E,
              !,
              *writeln(E)
          ;   writeln(E)
          )).

bash_cmd_out(Cmd, Output, Rc) :-
    *bcm("bash_cmd_out", Cmd),
    catch(( process_create(path(bash),
                           ["-c", Cmd],
                           [stdout(pipe(Out)), stderr(pipe(Out))]),
            read_string(Out, _, Output),
            close(Out),
            Rc=0
          ),
          error(E, _),
          (   process_error(_, exit(Rc))=E,
              !,
              *writeln(E)
          ;   writeln(E)
          )).

dtest :-
    write("-dtest"),
    nl,
    forall(src(Si),
           ( dhck(dh(Si, _)),
             writeln(Si)
           )),
    savedh.

bash_cmd_dir_out(Cmd, ADir, Output, Rc) :-
    *bcm("bash_cmd_dir_out", Cmd),
    catch(( process_create(path(bash),
                           ["-c", Cmd],
                           
                           [ cwd(ADir),
                             stdout(pipe(Out)),
                             stderr(pipe(Out))
                           ]),
            read_string(Out, _, Output),
            close(Out),
            Rc=0
          ),
          error(E, _),
          (   process_error(_, exit(Rc))=E,
              !,
              *writeln(E)
          ;   writeln(E)
          )).

bash_cmd_dir(Cmd, ADir, Rc) :-
    *bcm("bash_cmd_dir", Cmd),
    catch(( process_create(path(bash), ["-c", Cmd], [cwd(ADir)]),
            Rc=0
          ),
          error(E, _),
          (   process_error(_, exit(Rc))=E,
              !,
              *writeln(E)
          ;   writeln(E)
          )).

bash_cmd(Cmd, Rc) :-
    *bcm("bash_cmd", Cmd),
    catch(( process_create(path(bash), ["-c", Cmd], []),
            Rc=0
          ),
          error(E, _),
          (   process_error(_, exit(Rc))=E,
              !,
              *writeln(E)
          ;   writeln(E)
          )).

