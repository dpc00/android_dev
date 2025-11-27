import sys
from asyncio import create_subprocess_shell, wait, ensure_future
from asyncio.subprocess import PIPE, STDOUT

txt = ''
idel = 1


async def run(shell_command, cwd=None):
    global txt
    txt = ''
    p = await create_subprocess_shell(shell_command,
                                      cwd=cwd,
                                      stdout=PIPE,
                                      stderr=STDOUT)
    (so, se) = await p.communicate()
    if so:
        txt = so.decode()
        if txt:
            print(txt)
    return p.returncode


async def run1(shell_command, cwd=None):
    global txt
    txt = ''
    p = await create_subprocess_shell(shell_command,
                                      cwd=cwd,
                                      stdout=PIPE,
                                      stderr=STDOUT)
    (so, se) = await p.communicate()
    if so:
        txt = so.decode()
    return p.returncode


async def run2(shell_command, cwd=None):
    p = await create_subprocess_shell(shell_command, cwd=cwd)
    await p.communicate()
    return p.returncode


async def run3(shell_command, cwd=None):
    p = await create_subprocess_shell(shell_command,
                                      cwd=cwd,
                                      stdout=PIPE,
                                      stderr=STDOUT)
    future = ensure_future(p.wait())
    ic = 5 / idel

    rfuture = None

    async def readso():
        nonlocal ic, rfuture
        amtrd = 0
        if rfuture is None:
            rfuture = ensure_future(p.stdout.readline())
        done, pe = await wait([rfuture], timeout=idel)
        if rfuture in done:
            s = await rfuture
            if s and len(s):
                amtrd += len(s)
                sys.stdout.write(s.decode())
                sys.stdout.flush()
            ic -= idel
            rfuture = None
        else:
            ic -= idel
        print(ic * idel, amtrd)
        return amtrd

    while True:
        done, pe = await wait([future], timeout=idel)
        if future in done:
            while await readso():
                pass
            return p.returncode
        else:
            await readso()
        if ic <= 0:
            p.kill()
