'''
@author:     Phil

'''

import glob
import sys

import utils


def fl(spec):
    return glob.glob(spec)

def pause():
    utils.writedata('press enter...')
    input()

class Bat():
    @staticmethod
    def touch():
        import dirutils
        dirutils.touchBats()

    @staticmethod
    def backup():
        import copy_flash, utils
        d1 = utils.expES('%FLASH0%\\Projects\\tools\\.bat')
        d2 = utils.expES('%FLASH0%\\.bat')
        copy_flash.dirCopy(d1, d2)
        copy_flash.dirCopy(d2, d1)
        d3 = utils.expES('%FLASH0%\\Projects\\tools\\.lnk')
        d4 = utils.expES('%FLASH0%\\.lnk')
        copy_flash.dirCopy(d3, d4)
        copy_flash.dirCopy(d4, d3)

class Cpl():
    @staticmethod
    def hd():
        import cpl_hd
        cpl_hd.run()

    @staticmethod
    def flash():
        import cpl_flash
        cpl_flash.run()

    @staticmethod
    def bat():
        import cpl_bat
        cpl_bat.run()

class Flash_Backup():
    @staticmethod
    def full():
        import Dir, DirSync, Drive, os
        sda = utils.establish()
        Drive.getDrives(True)
        dir1 = Dir.fromPath(sda[0])
        sda = sda[1:]
        for sda1 in sda:
            dir2 = Dir.fromPath(sda1)
            if dir2 is None:
                return
            ds = DirSync.DirSync('CODE0->CODEn', dir1, dir2, clearstats=True)
            ds.run(includesubdirs=True)
        # Dir.saveDrives()

    @staticmethod
    def partial():
        import copy_flash
        copy_flash.fcopy2()

    @staticmethod
    def test():
        import copy_flash
        copy_flash.fcopy3()

    @staticmethod
    def dirsyncpro():
        # copy_flash.dsPro()
        pass

class Frege():
    @staticmethod
    def compile():
        from Dos4 import Dos4
        def fcompile(srcfile):
            return Dos4({
                'cmd': 'java.exe',
                'args': ['-Dfrege.javac=\\Programs\\jre1.8.0_73\\bin\\java.exe -jar ../ecj-4.5.1.jar -7 -encoding UTF-8', '-jar', '../frege-3.23.422-ga05a487.jar', '-d', 'out', srcfile],
                'collect': False,
                'echo': False,
                'oprint': True
            })
        v1 = fl('src/**/*.fr')
        for d in v1:
            fcompile(d)

class Git():
    @staticmethod
    def getRepos():
        from GitRepo import GitRepo
        import utils
        v1 = utils.prjList
        def run(prj):
            return GitRepo(wt=utils.prjDir(prj),
                    gd=utils.gitDir(prj)
                )
        v2 = map(run, v1)
        return list(v2)

    @staticmethod
    def backup():
        repos = Git.getRepos()
        for gr in repos:
            gr.backup()

    @staticmethod
    def status():
        repos = Git.getRepos()
        for gr in repos:
            gr.status()

    @staticmethod
    def reinit():
        repos = Git.getRepos()
        for gr in repos:
            gr.reInit()


class Java():
    @staticmethod
    def compile():
        from Dos4 import Dos4
        import utils
        def javacompile(prj, srcfiles):
            d1 = utils.prjDir('lib')
            d2 = utils.prjDir(prj) + '\\src'
            d3 = utils.prjDir(prj) + '\\out'
            return Dos4({
                'cmd': 'java.exe',
                'args': ['-jar', d1 + '\\ecj-4.5.1.jar',
                         '-sourcepath', d2,
                         '-cp', d3,
                         '-d', d3,
                         '-encoding', 'UTF-8', '-8', '-g', '-verbose']
                         + srcfiles,
                'collect': False,
                'echo': True,
                'oprint': True
            })
        v1 = utils.prjList
        for prj in v1:
            pd = utils.prjDir(prj)
            fl = glob.glob(pd + '\\src\\**\\*.java')
            if len(fl) > 0:
                javacompile(prj, fl)


'''
task('sublimetext', [],
    function() {
        var tn = this.fullName;
        jake.logger.log("'" + tn + "' starting");
        cf.sublimeText();
        jake.logger.log("'" + tn + "' done.");
    }, false
);
'''

class Typescript():
    @staticmethod
    def compile():
        from Dos4 import Dos4
        return Dos4({
            'cmd': 'tsc.cmd',
            'args': ['-p', '.'],
            'echo': True,
            'oprint': True
        })

class Root():
    @staticmethod
    def build():
        compile()

    @staticmethod
    def backups():
        Bat.backup()
        Git.backup()

    @staticmethod
    def compile():
        Frege.compile()
        Java.compile()
        Typescript.compile()

    @staticmethod
    def default():
        pass

    @staticmethod
    def disk_mon():
        from disk_mon import background
        background()



ftable = {
    'backups': Root.backups,
    'bat:backup': Bat.backup,
    'bat:touch': Bat.touch,
    'build': Root.build,
    'compile': Root.compile,
    'cpl:bat': Cpl.bat,
    'cpl:flash': Cpl.flash,
    'cpl:hd': Cpl.hd,
    'default': Root.default,
    'disk_mon': Root.disk_mon,
    'flash-backup:full': Flash_Backup.full,
    'flash-backup:partial': Flash_Backup.partial,
    'flash-backup:test': Flash_Backup.test,
    'frege:compile': Frege.compile,
    'git:backup': Git.backup,
    'git:reinit': Git.reinit,
    'git:status': Git.status,
    'java:compile': Java.compile,
    'typescript': Typescript.compile
}


def doCmd(cmd):
    #pr = cProfile.Profile()
    #pr.enable()
    import utils
    utils.log("'" + cmd + "' starting...")
    try:
        ftable[cmd]()
        utils.log("'" + cmd + "' done.")
    except Exception as e:
        utils.errlog(e)
        raise e
    #finally:
    #    pr.disable()
    #    s = io.StringIO()
    #    sort_by = 'tottime'
    #    ps = pstats.Stats(pr, stream=s).sort_stats(sort_by)
    #    ps.print_stats()
    #    print(s.getvalue())

def main(argv=None):  # IGNORE:C0111
    if not argv is None and  len(argv) > 1:
        for cmd in argv[1:]:
            if cmd in ftable:
                doCmd(cmd)
        return
    else:
        while True:
            import utils
            for f in ftable:
                utils.log(f)
            utils.writedata('\n')
            cmd = input('enter task or \'exit\':')
            while cmd == '':
                cmd = input('enter task or \'exit\':')
            if cmd == 'exit':
                return 0
            if cmd in ftable:
                doCmd(cmd)
            else:
                from Dos4 import Dos4
                Dos4({
                   'cmd': 'cmd.exe',
                   'args': ['/c'] + cmd.split(' '),
                   'echo': True,
                   'collect': False,
                   'oprint': True
                })

if __name__ == "__main__":
    sys.exit(main(sys.argv))