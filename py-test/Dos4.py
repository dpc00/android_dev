"""
Created on Jul 1, 2016

@author: Phil
"""

import subprocess
import utils
import re


class Dos4:
    def exec2(self):
        self.rejected = False
        if self.echo:
            cmdstr = self.cmd + " " + " ".join(self.args)
            utils.log(cmdstr + "\n")
        tcmd = [self.cmd] + self.args
        try:
            proc = subprocess.run(
                tcmd, shell=self.shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            self.proc = proc
            if self.collect or self.oprint:
                if self.collect:
                    self.outs += proc.stdout.decode()
                    self.outs += proc.stderr.decode()
                    self.outs = re.sub(r"\r\n", "\n", self.outs)
                if self.oprint:
                    utils.writedataindent(proc.stdout.decode())
                    utils.writedataindent(proc.stderr.decode())
            self.returncode = proc.returncode
            if proc.returncode != 0:
                self.rejected = True
        except Exception as e:
            utils.errlog(e)
            self.rejected = True
            self.returncode = proc.returncode

    def __init__(self, po):
        self.args = []
        self.cmd = ""
        self.collect = False
        self.echo = False
        self.outs = ""
        self.oprint = True
        self.proc = None
        self.shell = False
        for k in po.keys():
            self.__dict__[k] = po[k]
        self.exec2()

    def outs(self):
        return self.outs

    def rejected(self):
        return self.rejected
