:- writeln("-- git.pl --").
:- ensure_loaded(["gb_env.pl","funcs.pl","netup.pl"]).

diffcmd1('git diff --dirstat=files').
diffcmd2('git diff --dirstat=files --cached').

grlcmd(Rmt, Cmd) :- 
   nonvar(Rmt), 
   string_concat("git rev-list ",Rmt,S1),
   string_concat(S1, "/master...master", Cmd).

gpcmd(Rmt, Cmd) :-
   string_concat("git push ", Rmt, S1),
   string_concat(S1, " master", Cmd).
  
gscmd("git status --porcelain --untracked-files=all").
  
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

git_diff1(Wt) :-
    diffcmd1(Cmd),
    bash_cmd_dir_out(Cmd, Wt, Rv, Rc),
    (   Rc=\=0
    ->  write("gd1 rc: "),
        writeln(Rc),
        fail
    ;   string_length(Rv, 0)
    ->  fail
    ;   true
    ).

git_diff2(Wt) :-
    diffcmd2(Cmd),
    bash_cmd_dir_out(Cmd, Wt, Rv, Rc),
    (   Rc=\=0
    ->  write("gd2 rc: "),
        writeln(Rc),
        fail
    ;   string_length(Rv, 0)
    ->  fail
    ;   true
    ).

git_status(Wt, SLs) :-
    gscmd(Cmd),
    bash_cmd_dir_out(Cmd, Wt, Rv, Rc),
    (   Rc=\=0
    ->  write("gs rc: "),
        writeln(Rc),
        fail
    ;   string_length(Rv, 0)
    ->  SLs=[]
    ;   split_string(Rv, "\n", "\n", SLs)
    ).


getAdds(Wt, Al) :-
   git_status(Wt, SLs),
   include(proc_crit1, SLs, Al).

getCommits(Wt, Cl) :-
   git_status(Wt, SLs),
   include(proc_crit2, SLs, Cl).

getRevs(Wt, Rl, Rmt) :-
    grlcmd(Rmt, Cmd),
    bash_cmd_dir_out(Cmd, Wt, Rv, Rc),
    (   Rc=\=0
    ->  write("rl rc: "),
        writeln(Rc),
        fail
    ;   string_length(Rv, 0)
    ->  Rl=[]
    ;   split_string(Rv, "", "\n", Rl)
    ).

doAdds(Wt, Al) :-
   Al == [], !;
   [H|T] = Al,
   sub_string(H, 3, _, 0, Fn),
   write("Adding "),
   writeln(Fn),
   string_concat("git add -A ", Fn, Cmd),
   bash_cmd_dir(Cmd, Wt, Rc),
   (Rc =\= 0
    -> write("ga rc: "),
       write(Rc),
       fail
   ;   doAdds(Wt, T)
   ).

doCommit(Wt, Cl) :-
    (   Cl==[],
        !
    ;   write("Committing; causes: "),
        writeln(Cl),
        bash_cmd_dir("git commit -a -m git_pl", Wt, Rc),
        (   Rc=\=0
        ->  write("gc rc: "),
            writeln(Rc),
            fail
        ;   true
        )
    ).

chknet(Rmt) :-
   Rmt == 'local', !; netup.

doPush(Wt, Rl, Rmt) :-
    (   Rl==[],
        !
    ;   chknet(Rmt),
        write("Pushing "),
        write(Wt),
        write("->"),
        write(Rmt),
        write("; causes: "),
        writeln(Rl),
        gpcmd(Rmt, Cmd),
        bash_cmd_dir(Cmd, Wt, Rc),
        (   Rc=\=0
        ->  write("gp rc: "),
            writeln(Rc),
            fail
        ;   true
        )
    ).


