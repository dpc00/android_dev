'''
Created on Jul 12, 2016

@author: Phil
'''

import os
import re

import utils
from Dos4 import Dos4
import diskutils


class GitRepo():
    '''
    classdocs
    '''
    def __init__(self, wt='.', gd='.'):
        '''
        Constructor
        '''
        self.wt = wt
        self.gd = gd

    def gitcmd(self, args, opts):
        opts2 = {
            'cmd': 'git.exe',
            'args': ['--work-tree=' + self.wt, '--git-dir=' + self.gd] + args,
            'collect': False,
            'echo': False,
            'oprint': False
        }
        for k in ['collect', 'echo', 'oprint']:
            if k in opts:
                opts2[k] = opts[k]
        return Dos4(opts2)

    def dil(self):
        utils.log('delete index lock ' + self.wt + ', ' + self.gd)
        fn = self.gd + '\\index.lock'
        (e1, fe) = diskutils.fileExists(fn)
        if e1:
            return (e1, False)
        if fe:
            try:
                os.unlink(fn)
                # utils.log('unlinked ' + fn)
                return (None, True)
            except Exception as e:
                utils.errlog(e)
                return (e, None)
        else:
            return (None, False)


    def status(self):
        utils.log('git status ' + self.wt + ', ' + self.gd)
        utils.log()
        rv = self.gitcmd(['status', '--porcelain', '--untracked-files=all'], {
            'echo': False,
            'collect': True,
            'oprint': True
        })
        if rv.rejected:
            return (OSError(rv.returncode, 'git status error'), None)
        s1 = re.split('[\r\n]+', rv.outs)
        if len(s1) == 0:
            return (None, [])
        def run(l):
            return len(l) != 0
        return (None, [l[3:] for l in s1 if run(l)])

    def add(self, sa):
        utils.log('git add ' + self.wt + ', ' + self.gd)
        rv1 = self.gitcmd(['add'] + sa, {
            'echo': False,
            'collect': False,
            'oprint': True
        })
        if rv1.rejected:
            utils.log(rv1.outs)
            fc = 0
            for f in sa:
                rv2 = self.gitcmd(['add', f], {
                            'echo': False,
                            'collect': False,
                            'oprint': True
                        })
                if rv2.rejected:
                    utils.log(rv2.outs)
                else:
                    fc += 1
            if fc > 0:
                return (None, fc)
            else:
                return (OSError('git multiple add'), None)
        else:
            return (None, len(sa))

    def commit(self):
        utils.log('git commit ' + self.wt + ', ' + self.gd)
        rv = self.gitcmd(['commit', '-a', '-m', '\'abcde\''], {
            'echo': False,
            'collect': False,
            'oprint': True
        })
        if rv.rejected:
            return (OSError(rv.returncode, 'git commit error'), None)
        else:
            return (None, True)

    def push(self):
        utils.log('git push ' + self.wt + ', ' + self.gd)
        rv = self.gitcmd(['push', 'origin', 'master', '--porcelain', '--force'], {
            'echo': False,
            'collect': False,
            'oprint': True
        })
        if rv.rejected:
            return (OSError(rv.returncode, 'git push error'), None)
        else:
            return (None, True)

    def backup(self):
        (e1, _) = self.dil()
        if e1:
            utils.log('dil error')
            return (e1, None)
        (e2, sa) = self.status()
        if e2:
            utils.log('git status(1) error')
            return (e2, None)
        if len(sa) != 0:
            (e3, _) = self.add(sa)
            if e3:
                utils.log('git add error')
                return (e3, None)
        (e4, sa) = self.status()
        if e4:
            utils.log('git status(2) error')
            return (e4, None)
        if len(sa) != 0:
            (e5, _) = self.commit()
            if e5:
                utils.log('git commit error')
                return (e5, None)
        (e6, _) = self.push()
        if e6:
            utils.log('git push error')
            return (e6, None)
        return (None, True)

    def reInit(self):
        from Dir import Dir, fromPath
        try:
            # fromPath(self.gd).delete()
            # utils.log('git init ' + self.wt + ', ' + self.gd)
            # rv = self.gitcmd(['init'], {
            #     'echo': False,
            #     'collect': False,
            #     'oprint': True
            # })
            # if rv.rejected:
            #     return (OSError(rv.returncode, 'git init error'), None)
            # else:
            #     return (None, True)
            # (e2, sa) = self.status()
            # if e2:
            #     utils.log('git status error')
            #     return (e2, None)
            # if len(sa) == 0:
            #     utils.log('git status returns no files')
            #     return (None, None)
            # (e3, _) = self.add(sa)
            # if e3:
            #     utils.log('git add error')
            #     return (e3, None)
            # (e4, _) = self.commit()
            # if e4:
            #     utils.log('git commit error')
            #     return (e4, None)
            # rv = self.gitcmd(['remote','add','origin', 'http://dpchitester:dpcarc@bitbucket.org/dpchitester/' + os.path.basename(self.wt) + '.git'], {
            #     'echo': False,
            #     'collect': False,
            #     'oprint': True
            # })
            # if rv.rejected:
            #     return (OSError(rv.returncode, 'git add remote error'), None)
            # else:
            #     return (None, True)
            utils.log('git push ' + self.wt + ', ' + self.gd)
            rv = self.gitcmd(['push', '--force', '--mirror', 'origin'], {
                'echo': False,
                'collect': False,
                'oprint': True
            })
            if rv.rejected:
                return (OSError(rv.returncode, 'git push error'), None)
            else:
                return (None, True)
        except OSError:
            pass
if __name__ == "__main__":
    from GitRepo import GitRepo
    def getRepos():
        v1 = utils.prjList
        def run(prj):
            return GitRepo(wt=utils.prjDir(prj),
                    gd=utils.gitDir(prj)
                )
        v2 = map(run, v1)
        return list(v2)
    repos = getRepos()
    for gr in repos:
        gr.backup()
