from autobahn.asyncio.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory

from MonPaquet import json_parser
#from MonPaquet import gpio_controler


class MyServerProtocol(WebSocketServerProtocol):

    def setGPIOList(self, GPIOList):
        self.myGPIOs = GPIOList
        #plus utilisé

    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))
        self.myGPIOs = dict()
        json_parser.readconfig(self.myGPIOs, "gpio_def.xml")
        # gpio_controler.setupOutput(self.myGPIOs)

    def onOpen(self):
        print("WebSocket connection open.")

    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
            print("Text message received: {0}".format(payload.decode('utf8')))

        # echo back message verbatim
        # self.sendMessage(payload, isBinary)
        #jsonStr = json.loads(payload.decode('utf8'))

        jsonStr2 = payload.decode('utf8')

        json_parser.read_json(jsonStr2, self.myGPIOs)

        for keys in self.myGPIOs.keys():
            print(keys + " vaut : " + self.myGPIOs[keys].value)

        # gpio_controler.apply(self.myGPIOs)

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))
        # gpio_controler.close()

if __name__ == '__main__':
    import asyncio

    factory = WebSocketServerFactory(u"ws://127.0.0.1:9000")
    factory.protocol = MyServerProtocol

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
