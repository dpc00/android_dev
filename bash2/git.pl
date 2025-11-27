grlcmd('git rev-list origin/master..master').
gscmd('git status --porcelain --untracked-files=all').
    
add_crit(L) :- \+member(L, [" ", "D", "R"]).

comm_crit(L) :- \+member(L, [" "]).

proc_crit1(H) :-
    string(H),
    sub_string(H, 1, 1, _, C2),
    add_crit(C2).

proc_crit2(H) :-
    string(H),
    sub_string(H, 0, 1, _, C1),
    comm_crit(C1).

git_status(Wt, SLs) :-
    gscmd(Cmd),
    notrace((bash_cmd_dir_out(Cmd, Wt, Rv),
    \+string_length(Rv, 0),
    split_string(Rv, "\n", "\n", SLs))).
git_status(_, []).

getAdds(Wt, Al) :-
    notrace((git_status(Wt, SLs),
    include(proc_crit1, SLs, Al))).

getCommits(Wt, Cl) :-
    notrace((git_status(Wt, SLs),
    include(proc_crit2, SLs, Cl))).

getRevs(Wt, Rl) :-
    notrace((grlcmd(Cmd),
    bash_cmd_dir_out(Cmd, Wt, Rv),
    \+string_length(Rv, 0),
    split_string(Rv, "", "\n", Rl))).
getRevs(_, []).

doAdds(_, []).
doAdds(Wt, [H|T]) :-
    sub_string(H, 3, _, 0, Fn),
    write("Adding "),
    writeln(Fn),
    notrace((concat('git add -A ', Fn, Cmd),
    bash_cmd_dir(Cmd, Wt))),
    doAdds(Wt, T).

doCommit(_, []).
doCommit(Wt, Cl) :-
    writeln("Committing; causes: "),
    writeln(Cl),
    notrace(bash_cmd_dir('git commit -a -m git_pl', Wt)).

doPush(_, []).
doPush(Wt, Rl) :-
    netup,
    write("Pushing "), write(Wt), writeln("; causes: "), writeln(Rl),
    notrace(bash_cmd_dir('git push origin master', Wt)).
