clear
echo '' > rufftest.txt
sis=$(ruff linter | awk '{print $1}')
for si in ${sis[@]}
do
 echo --------$si-------- >>rufftest.txt
 ruff check --select $si --diff *.py >>rufftest.txt
done