from MonPaquet import client_01 as client
#from MonPaquet import Cgpio
from MonPaquet import json_parser


if __name__ == '__main__':

    my_gpios = []

    json_parser.readconfig(my_gpios, "gpio_def_test.xml")

    ch = "nom : %s    valeur : %s"

    for i in my_gpios:
        ch2 = ch % (i.nom, i.value)
        print(ch2)

    jsonStr = json_parser.write_json(my_gpios)

    print("-----1-----")

    try:
        import asyncio
    except ImportError:
        # Trollius >= 0.3 was renamed
        import trollius as asyncio

    factory = client.WebSocketClientFactory(u"ws://127.0.0.1:9000")
    factory.protocol = client.MyClientProtocol

    client.MyClientProtocol.setJson(factory.protocol,jsonStr)

    loop = asyncio.get_event_loop()
    coro = loop.create_connection(factory, '127.0.0.1', 9000)

    loop.run_until_complete(coro)

    #client.MyClientProtocol.sendExtJson(factory.protocol, jsonStr)

    #factory.protocol.sendExtJson(factory.protocol, jsonStr)
    #factory.protocol.sendMessage(factory.protocol, jsonStr.encode('utf8'))

    loop.run_forever()
    loop.close()


