from autobahn.asyncio.websocket import WebSocketClientProtocol, \
    WebSocketClientFactory


class BancClientProtocol(WebSocketClientProtocol):

    serv = list()
    InputJson = str()

    def onConnect(self, response):
        print("Server connected: {0}".format(response.peer))

    def onOpen(self):
        print("WebSocket connection open.")
        self.serv.append(self)
        self.factory.loop.call_soon(self.factory.loop.stop)
        # start sending messages every second ..
        #hello()

    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
            print("Text message received: {0}".format(payload.decode('utf8')))
        self.factory.loop.call_soon(self.factory.loop.stop)
        # self.factory.loop.stop
        BancClientProtocol.setInputJson(payload, decode = True)

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))

    @classmethod
    def Quit(cls):
        for c in set(cls.serv):
            c.sendClose()

    @classmethod
    def listen(cls):
        for c in set(cls.serv):
            c.factory.loop.run_forever()
            c.factory.loop.call_later(delay=0.300, callback= c.factory.loop.stop)

    @classmethod
    def getInputJson(cls):
        return cls.InputJson

    @classmethod
    def setInputJson(cls, InJson, decode = False):
        if decode:
            cls.InputJson = InJson.decode('utf8')
        else :
            cls.InputJson = InJson


if __name__ == '__main__':

    try:
        import asyncio
    except ImportError:
        # Trollius >= 0.3 was renamed
        import trollius as asyncio

    factory = WebSocketClientFactory(u"ws://127.0.0.1:9001")
    # factory = WebSocketClientFactory(u"ws://10.106.76.45:9000")
    factory.protocol = BancClientProtocol

    loop = asyncio.get_event_loop()
    # coro = loop.create_connection(factory, '10.106.76.45', 9000)
    coro = loop.create_connection(factory, '127.0.0.1', 9001)
    loop.run_until_complete(coro)
    #loop.run_forever()
    loop.close()