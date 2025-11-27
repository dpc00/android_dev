from asyncio import create_subprocess_shell, run, open_connection, wait_for
from asyncio.subprocess import PIPE


async def netup():
    con = open_connection("www.bitbucket.org",80)
    try:
        (r, w) = await wait_for(con, 2)
        w.write(b'HEAD')
        w.write(b'/')
        await w.drain()
        w.close()
        await w.wait_closed()
        #await r.read()
        await netup2()
        return True
    except Exception as e:
        print('nu exception:',e)
        return False

cmd2 = "termux-wifi-connectioninfo | jq -r '.ip'"

async def netup2():
    p = await create_subprocess_shell(cmd2, stdout=PIPE)
    await p.wait()
    rv = await p.stdout.read()
    rv = rv.decode().strip()
    print(rv)
    return rv != '0.0.0.0'


if __name__ == '__main__':
    print(run(netup()))
