# !/usr/bin/python3.4

from MonPaquet import serveur_01

if __name__ == '__main__':

    import asyncio

    factory = serveur_01.WebSocketServerFactory(u"ws://127.23.240.29:9000")
    # factory = serveur_01.WebSocketServerFactory(u"ws://127.0.0.1:9000")
    factory.protocol = serveur_01.MyServerProtocol

    loop = asyncio.get_event_loop()
    coro = loop.create_server(factory, '0.0.0.0', 9000)
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.close()
        loop.close()
