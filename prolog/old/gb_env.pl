:- write("-- gb_env.pl --"), nl.

 :- op(920, fy, *).
*_. 

:- multifile pre/2.
:- multifile pdir/2.

:- dynamic dn1/1.
:- dynamic dstts/3.
:- dynamic sn1/1.
:- dynamic srcts/2.

svcs([db, od, gd]).

snm(db, "DropBox").
snm(gd, "GoogleDrive").
snm(od, "OneDrive").

snms(L) :-
	findall(
		Sn,
		snm(_, Sn),
		L
	).


svc(X) :-
    svcs(L),
    member(X, L).

pre(proj, "/sdcard/projects").
pre('FLAGS', X) :-
    getenv('HOME', X1),
    string_concat(X1, "", X).
pre(rtbk, X) :-
    pre('FLAGS', X1),
    string_concat(X1, "/.rtbk", X).
pre(ct, X) :-
    pre('FLAGS', X1),
    string_concat(X1, "/.ct", X).
pre(bklog, X) :-
    pre('FLAGS', X1),
    string_concat(X1, "/.bklog", X).
pre(bkx, X) :-
    pre('FLAGS', X1),
    string_concat(X1, "/.bkx", X).
pre(dh, X) :-
    pre('FLAGS', X1),
    string_concat(X1, "/.dh", X).

tdir(home, X) :-
    getenv('HOME', X).
tdir(bin, X) :-
    tdir(home, X1),
    string_concat(X1, "/bin", X).
tdir(sh, X) :-
    tdir(bin, X1),
    string_concat(X1, "/sh", X).
tdir(pl, X) :-
    tdir(bin, X1),
    string_concat(X1, "/pl", X).
tdir(py, X) :-
    tdir(bin, X1),
    string_concat(X1, "/py", X).
tdir(backups, "/sdcard/backups").
tdir(fdbak, X) :-
    pdir(proj, X1),
    string_concat(X1, "/fdb", X).
tdir(scrdev, X) :-
    pdir(scrdev, X).
tdir(rclone, X) :-
    tdir(home, X1),
    string_concat(X1, "/.config/rclone", X).
    
pdir(docs, "/sdcard/Documents").
pdir(refs, "/sdcard/Reference").
pdir(proj, "/sdcard/projects").
pdir(fdb, "/sdcard/Documents/Finance.db").
pdir(zip, "/sdcard/backups/projects.zip").
pdir(blog, X) :-
    pdir(proj, X1),
    string_concat(X1, "/blog", X).
pdir(fdbak, X) :-
    pdir(proj, X1),
    string_concat(X1, "/fdb", X).
pdir(scrdev, X) :-
    pdir(proj, X1),
    string_concat(X1, "/bash", X).
pdir(bash2, X) :-
    pdir(proj, X1),
    string_concat(X1, "/bash2", X).
pdir(pro, X) :-
    pdir(proj, X1),
    string_concat(X1, "/prolog", X).
pdir(js, X) :-
    pdir(proj, X1),
    string_concat(X1, "/js", X).
pdir(pyth, X) :-
    pdir(proj, X1),
    string_concat(X1, "/python", X).
pdir(git, X) :-
    pdir(proj, X1),
    string_concat(X1, "/.git", X).
pdir(pi, X) :-
    pdir(proj, X1),
    string_concat(X1, "/prolog_indent", X).
pdir(rclone_as_src, X) :-
    tdir(rclone, X).


codes([blog, fdbak, scrdev, bash2, pyth, pro, js]).

srcs(L2) :-
    codes(L1),
    union([fdb, docs, git, zip, rclone_as_src, refs], L1, L2).

src(X) :-
    srcs(L),
    member(X, L).

code(X) :-
    codes(L),
    member(X, L).

worktree(Wt) :-
    pdir(proj, Wt),
    !.

opdep(scpy, Di, Si, Di, Si, [files(Fl)]) :-
    Di=[rclone],
    Si=[scrdev],
    Fl=["rclone.conf"].
opdep(scpy, Di, Si, Di, Si, [files(Fl)]) :-
    Di=[scrdev],
    Si=[rclone_as_src],
    Fl=["rclone.conf"].
opdep(scpy, Di, Si, Di, Si, [files(Fl)]) :-
    Di=[home],
    Si=[scrdev],
    Fl=[".termux/**", ".bash*", ".swi*", ".profile", ".clang-format", "rsyncd.conf"].
opdep(scpy, Di, Si, Di, Si, [files(Fl)]) :-
    Di=[etc],
    Si=[scrdev],
    Fl=["rsyncd.conf", "rsyncd.secrets"].
opdep(scpy, Di, Si, Di, Si, [files(Fl), exec(true)]) :-
    Di=[bin],
    Si=[scrdev],
    Fl=["termux-*"].
opdep(scpy, Di, Si, Di, Si, [files(Fl), exec(true)]) :-
    Di=[sh],
    Si=[scrdev],
    Fl=["*.sh", "*.env"].
opdep(scpy, Di, Si, Di, Si, [files(Fl), exec(true)]) :-
    Di=[py],
    Si=[pyth],
    Fl=["*.py"].
opdep(scpy, Di, Si, Di, Si, [files(Fl), exec(true)]) :-
    Di=[pl],
    Si=[pro],
    Fl=["*.pl"].
opdep(scpy, Di, Si, Di, Sd, [files(Fl)]) :-
    Di=[fdbak],
    Si=[fdb],
    Sd=[docs],
    Fl=["Finance.db"].
opdep(scpy, Di, Si, Di, Sd, [files(Fl)]) :-
    Di=[backups],
    Si=[fdb],
    Sd=[docs],
    Fl=["Finance.db"].

opdep(gitbackup, Di, Si, [], [], [wt(Wt), add(true), commit(true)]) :-
    Di=[git],
    codes(Si),
    worktree(Wt).
opdep(gitbackup, Di, Si, [], [], [wt(Wt), rmt(local), push(true)]) :-
    Di=[local],
    Si=[git],
    worktree(Wt).
opdep(gitbackup, Di, Si, [], [], [wt(Wt), rmt(bitbucket), push(true)]) :-
    Di=[bitbucket],
    Si=[git],
    worktree(Wt).

opdep(csbackup, Di, Si, [], [], []) :-
    svcs(Di),
    codes(L1),
    union(L1, [], Si).

opdep(mkzip, Di, Si, Dd, Sd, [zipfile(Zf)]) :-
    Di=[zip],
    codes(Si),
    Dd=[backups],
    Sd=[proj],
    Zf="projects.zip".

dep(A, B) :-
	opdep(_, [H1|T1],[H2|T2], _,_,_),
	member(A, [H1|T1]),
	member(B, [H2|T2]).
	
:- dynamic dn1/1.
:- dynamic dstts/3.
:- dynamic sn1/1.
:- dynamic srcts/2.
:- retractall(sn1/1), retractall(srcts/2), assert(sn1(1)).
:- retractall(dn1/1), retractall(dstts/3), assert(dn1(1)).

:- ensure_loaded(['tstamp.pl']).
:-
  forall(
      src(S),
      (   sn1(N1),
          retract(sn1(N1)),
          N2 is N1 + 1,
          assert(sn1(N2)),
          assert(srcts(S,N1)),
          tstime_m('rtbk',N1, _)
      )
  ).

:-
  forall(
      dep(T, S),
      (   dn1(N1),
          retract(dn1(N1)),
          N2 is N1 + 1,
          assert(dn1(N2)),
          assert(dstts(T,S,N1)),
          tstime_m('ct',N1, _)
      )
  ).

:- compile_predicates([srcts/2, dstts/3]).
