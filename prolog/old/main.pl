#!/data/data/com.termux/files/usr/bin/env swipl
:- initialization(main, main).

:- writeln("-- main.pl --").

:- consult(
 ["gb_env.pl",
  "funcs.pl",
  "fcutils.pl",
  "tstamp.pl",
  "dhash.pl",
  "netup.pl",
  "status.pl",
  "scpy.pl",
  "csbackups.pl",
  "git.pl",
  "gitbackup.pl",
  "opts.pl",
  "projback.pl",
  "rfmt2.pl"
]).

func(C) :-
    writev(C, 'C'),
    term_to_atom(T, C),
    writev(T, 'T'),
    nl,
    once(T).

main([]) :-
	dhset(rclone_as_src),
    !.
main([H|T]) :-
    catch(func(H),
          error(E, C),
          ( writev(E, 'E'),
            writev(C, 'C'),
            nl
          )),
    main(T).

