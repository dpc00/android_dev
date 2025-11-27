import sys
from pathlib import Path

from bowler import Query

old_name, new_name = sys.argv[1:]

print(old_name, "->", new_name)

(
    Query(["."], filename_matcher=lambda fn: len(Path(fn).parts) == 1)
    .select_function(old_name)
    .rename(new_name)
    .idiff()
)
