from autobahn.asyncio.websocket import WebSocketClientProtocol, \
    WebSocketClientFactory


class SysClientProtocol(WebSocketClientProtocol):

    serv = list()

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

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))


    @classmethod
    def sendExtJson(cls, jsonString):
        if isinstance(jsonString,str):
            payload = jsonString.encode('utf8')
            #print("json str")
            #print(str(type(payload)))
        elif isinstance(jsonString,bytes):
            payload = jsonString
            #print("json deja bytes")
        else :
            print("sendExtJson input error")

        #print("serv size : " + str(cls.serv.__len__()))
        for c in set(cls.serv):
            c.sendMessage(payload)
            #print("message send")

    def sendIntJson(self):
        payload = self.jsonStr.encode('utf8')
        self.sendMessage(payload)

    def setJson(self, jsonString):
        self.jsonStr = jsonString

    @classmethod
    def Quit(cls):
        for c in set(cls.serv):
            c.sendClose()

if __name__ == '__main__':

    try:
        import asyncio
    except ImportError:
        # Trollius >= 0.3 was renamed
        import trollius as asyncio

    factory = WebSocketClientFactory(u"ws://127.0.0.1:9000")
    # factory = WebSocketClientFactory(u"ws://10.106.76.45:9000")
    factory.protocol = SysClientProtocol

    loop = asyncio.get_event_loop()
    # coro = loop.create_connection(factory, '10.106.76.45', 9000)
    coro = loop.create_connection(factory, '127.0.0.1', 9000)
    loop.run_until_complete(coro)
    #loop.run_forever()
    loop.close()