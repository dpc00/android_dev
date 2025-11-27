pushd ~/projects/pybackup
pf=*.py
pylint --output-format=json:tool/lint-all.json,text:tool/lint-all.txt --reports=y $pf
python tool/lint-all-sort.py
popd
