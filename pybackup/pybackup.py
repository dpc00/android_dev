#!/data/data/com.termux/files/usr/bin/env python

from threading import Thread

import config
import ldsv as ls
from opexec import clean, opExec
from status import updatets

th3 = None


def rt2():
    global th1
    itc = 0
    while True:
        itc += 1
        cl = clean()
        if cl:
            print("no backups appear pending")
            break
        else:
            print("backups appear pending")
            opExec()


def main():
    global th3
    print("-main")
    config.initConfig()
    try:
        print("-main-2")
        updatets(0)
        print("-main-3")
        th3 = Thread(target=ls.save_bp)
        th3.start()
        print("-main-4")
        rt2()
        print("-main-5")
        config.quit_ev.set()
    except KeyboardInterrupt as exc:
        print(exc)
    finally:
        print("-main-6")
        if th3 and th3.is_alive():
            config.quit_ev.set()
            th3.join()


if __name__ == "__main__":
    main()
