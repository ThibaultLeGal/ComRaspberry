from MonPaquet import serveur_01
#from MonPaquet import Cgpio
from MonPaquet import json_parser


if __name__ == '__main__':

    my_gpios = []

    json_parser.readconfig(my_gpios, "gpio_def.xml")

    ch = "nom : %s    valeur : %s"

    for i in my_gpios:
        ch2 = ch % (i.nom, i.value)
        print(ch2)

    print("-----1-----")

    import asyncio

    factory = serveur_01.WebSocketServerFactory(u"ws://127.0.0.1:9000")
    factory.protocol = serveur_01.MyServerProtocol

    loop = asyncio.get_event_loop()
    coro = loop.create_server(factory, '127.0.0.1', 9000)
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.close()
        loop.close()