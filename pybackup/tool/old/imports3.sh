python -m snakefood3 $(realpath '.')/.. pybackup>imports.dot
dot -Tsvg -o imports.svg imports.dot
