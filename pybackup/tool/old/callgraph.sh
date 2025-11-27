clear
python -m pybackup
gprof2dot -z pybackup:140:main -f pstats -o temp.gv temp.pstat
dot -Tsvg -o temp.svg temp.gv

