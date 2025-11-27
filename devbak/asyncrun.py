import asyncio
from asyncio.subprocess import PIPE, STDOUT
from asyncio import create_subprocess_shell


async def run(shell_command, cwd=None):
    p = await create_subprocess_shell(shell_command, cwd=cwd)
    await p.wait()
    return p.returncode
