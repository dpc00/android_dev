bash_cmd(Cmd2) :- 
    process_create(
        path(bash),
        ['-c', Cmd2],
        []).

bash_cmd_out(Cmd2, Output) :- 
    process_create(
        path(bash),
        ['-c', Cmd2],
        [stdout(pipe(Out)),
            stderr(pipe(Out))]),
    read_string(Out, _, Output),
    close(Out).

bash_cmd_dir(Cmd2, ADir) :- 
    process_create(
        path(bash),
        ['-c', Cmd2],
        [cwd(ADir)]).

bash_cmd_dir_out(Cmd2, ADir, Output) :-
    process_create(
        path(bash),
        ['-c',Cmd2],
        [cwd(ADir),
            stdout(pipe(Out)),
            stderr(pipe(Out))]),
    read_string(Out, _, Output),
    close(Out).

filetime(Fn, Ft) :- 
    concat('stat -c %Y ', Fn, Cmd),
    notrace((bash_cmd_out(Cmd, Rv),
    split_string(Rv, '\n', '\n', [Fts]),
    number_chars(Ft, Fts))).

older(F1, F2) :-
    filetime(F1, Ft1),
    filetime(F2, Ft2),
    Ft1 < Ft2.

newer(F1, F2) :-
    filetime(F1, Ft1),
    filetime(F2, Ft2),
    Ft1 > Ft2.

flag(N, Fn) :- number_string(N, S), concat('~/tstamps/.ct', S, Fn).
isdirty(N) :- flag(N, Fn), older(Fn, '~/tstamps/.rtbk').
touch(N) :- flag(N, Fn), concat('touch ', Fn, Cmd), bash_cmd(Cmd).

nucmd('curl -s --head --request GET www.google.com | grep "200 OK"').

netup :- nucmd(Cmd), shell(Cmd, 0).
