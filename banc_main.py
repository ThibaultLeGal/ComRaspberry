# !/usr/bin/python3.4

from MonPaquet import serveur_banc

if __name__ == '__main__':

    import asyncio

    factory = serveur_banc.WebSocketServerFactory(u"ws://127.23.240.29:9001")
    # factory = serveur_banc.WebSocketServerFactory(u"ws://127.0.0.1:9001")
    factory.protocol = serveur_banc.MyServerProtocol

    loop = asyncio.get_event_loop()
    coro = loop.create_server(factory, '0.0.0.0', 9001)
    server = loop.run_until_complete(coro)


    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.close()
        loop.close()
