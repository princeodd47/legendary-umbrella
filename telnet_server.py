import asyncio, telnetlib3

clients = []

@asyncio.coroutine
def shell(reader, writer):
    clients.append(writer)
    writer.write('\r\nWould you like to play a game? ')
    character = None
    cmd = ""
    while True:
        character = yield from reader.read(1)
        print(character)
        writer.write(character)
        if character == '\r':
            handle_cmd(cmd)
        else:
            cmd += character

def handle_cmd(cmd):
    print('cmd')
    if cmd.startswith('say '):
        print('say start')
        for client in clients:
            client.write(cmd)
    elif cmd == 'quit':
        print('quit start')
        yield from writer.drain()
        writer.close()

loop = asyncio.get_event_loop()
coro = telnetlib3.create_server(port=6023, shell=shell)
server = loop.run_until_complete(coro)
loop.run_until_complete(server.wait_closed())
