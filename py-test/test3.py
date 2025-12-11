import fileinput
import os

import Dir


def cf1(s, d):
    os.system("copy " + s + " " + d)


def run(p):
    dl = fileinput.input(p)
    for l in dl:
        print("\t" + l)


bp1 = Dir.findDL("CODE0") + "\\Programs"
bp2 = ""
lfbn = "fb_fci.txt"
