n=1
for pf in *.py;
do
    echo "Lint file $n: $pf"
    pylint $pf >> lint-all.txt
    n = $(( n + 1))
done
