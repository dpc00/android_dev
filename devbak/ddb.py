import subprocess
import json

dircmd1 = 'ls -AgGlR --block-size=1 --time-style=+%s --color=never '
dircmd2_1 = ['rclone', 'lsf']
dircmd2_2 = ['--recursive', '--format', 'pst', '--files-only']
dircmd2ex = ['--exclude', ".git/**", '--exclude', "__pycache__/**"]


def cdircmd1(dir):
    cmd = dircmd1 + str(dir)
    return cmd.split()


def cdircmd2(dir):
    cmd = dircmd2_1 + [str(dir)]
    cmd += dircmd2_2
    if not dir.is_file():
        cmd += dircmd2ex
    return cmd


dircmd = cdircmd2


def getdll(dir):
    print('getdll', str(dir))
    cmd = dircmd(dir)
    pp = subprocess.run(cmd, capture_output=True)
    if pp.returncode == 0:
        st = pp.stdout.decode()
        st = st.splitlines()
        st.sort()
        return st
    else:
        return None


def getdlstr(dir):
    st = getdll(dir)
    if st is not None:
        st = '\n'.join(st)
        return st.encode()
    else:
        return b''
