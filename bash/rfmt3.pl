#!/data/data/com.termux/files/usr/bin/env swipl
:- write("--rfmt3.pl--"), nl.


:- ensure_loaded(['gb_env.pl']).
% :- use_module('indent').

indent(Fn1,Fn2) :-
    copy_file(Fn1, Fn2),
    concat("clang-format -i ", Fn2),
    time_file(Fn1, Ft1),
    set_time_file(Fn2, [], [modified(Ft1)]).
    
dofiles([]) :-
    writeln("done.").
dofiles([Fn1|T]) :-
    string_concat(Fn1, ".rf", Fn2),
    writeln(Fn2),
    (   indent(Fn1, Fn2)
    ->  dofiles(T)
    ;   dofiles(T)
    ).

rf_files(Fl) :-
    pdir(pro, PDir),
    string_concat(PDir, "/*.pl", PSpec),
    expand_file_name(PSpec, Fl).

rfmt3 :-
    rf_files(SLs),
    writeln("-rfmt"),
    dofiles(SLs).

