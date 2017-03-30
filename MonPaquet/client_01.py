from autobahn.asyncio.websocket import WebSocketClientProtocol, \
    WebSocketClientFactory


class MyClientProtocol(WebSocketClientProtocol):

    def onConnect(self, response):
        print("Server connected: {0}".format(response.peer))

    def onOpen(self):
        print("WebSocket connection open.")

        def hello():
            self.sendIntJson()

            self.factory.loop.call_later(5, hello)
        # start sending messages every second ..
        hello()

    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
            print("Text message received: {0}".format(payload.decode('utf8')))

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))

    def sendExtJson(self, jsonString):
        if isinstance(jsonString,str):
            payload = jsonString.encode('utf8')
            print("json str")
            print(str(type(payload)))
        elif isinstance(jsonString,bytes):
            payload = jsonString
            print("json deja bytes")
        else :
            print("what?")
        self.sendMessage(self, payload = payload, isBinary = False)

    def sendIntJson(self):
        payload = self.jsonStr.encode('utf8')
        self.sendMessage(payload)

    def setJson(self, jsonString):
        self.jsonStr = jsonString


if __name__ == '__main__':

    try:
        import asyncio
    except ImportError:
        # Trollius >= 0.3 was renamed
        import trollius as asyncio

    factory = WebSocketClientFactory(u"ws://127.0.0.1:9000")
    # factory = WebSocketClientFactory(u"ws://10.106.76.45:9000")
    factory.protocol = MyClientProtocol

    loop = asyncio.get_event_loop()
    # coro = loop.create_connection(factory, '10.106.76.45', 9000)
    coro = loop.create_connection(factory, '127.0.0.1', 9000)
    loop.run_until_complete(coro)
    loop.run_forever()
    loop.close()