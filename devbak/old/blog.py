#!/data/data/com.termux/files/usr/bin/env python3

import os
import argparse


def start():
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", nargs='*', default=0, type=float, dest='clst')
    ap.add_argument("-f", nargs='*', default=0, type=float, dest='flst')
    ap.add_argument("-s", nargs='*', default=0, type=float, dest='slst')
    args = ap.parse_args()
    print(args)


start()
