#!/data/data/com.termux/files/usr/bin/env swipl
:- writeln("-- netup.pl --").

:- ensure_loaded(["gb_env.pl","funcs.pl"]).

% nucmd("curl -s --head --request GET www.google.com | grep \"200 OK\"").
% netup :- nucmd(Cmd), shell(Cmd, 0).
% "dig @8.8.4.4 +notcp www.google.com 2>&1 | grep -q \"status: NOERROR\""

netup :-
    *writeln("-netup"),
    *srun("[ \"\"$(termux-wifi-connectioninfo | jq -r '.ip')\"\" != \"\"0.0.0.0\"\" ]",
         Rc),
    *netup(Rc).

netup(0) :-
    !.
netup(Rc) :-
    write("netup rc: "),
    writeln(Rc).

