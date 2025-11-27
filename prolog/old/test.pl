
process(Str) :-
    prolog_read_source_term(Str, Term, Expanded, [variable_names(Vars)]),
    (   Term == end_of_file ->
        nl
    ;   writeln(Term),
        writeln(Vars),
        nl,
        process(Str)
    ).

test :-
    prolog_open_source('csbackups.pl', Str),
    process(Str),
    prolog_close_source(Str).