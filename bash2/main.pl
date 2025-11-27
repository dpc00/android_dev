#!/bin/swipl

project('bash').
project('blog').

worktree(Wt) :-
    notrace((project(P1),
    getenv('proj', S1),
    concat(S1, '/', S2),
    concat(S2, P1, Wt))).

:- ["bin/misc.pl"].
:- ["bin/git.pl"].

gud1(Wt) :- getAdds(Wt, Al), doAdds(Wt, Al).
gud2(Wt) :- getCommits(Wt, Cl), doCommit(Wt, Cl).
gud3(Wt) :- getRevs(Wt, Rl), doPush(Wt, Rl).

gud(Wt) :- gud1(Wt), gud2(Wt), gud3(Wt).

u2d :- worktree(Wt), writeln(Wt), gud(Wt), fail.

%___

