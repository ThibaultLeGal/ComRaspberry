from autobahn.asyncio.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory
import RPi.GPIO as GPIO
from MonPaquet import json_parser
from MonPaquet import gpio_controler


class MyServerProtocol(WebSocketServerProtocol):

    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))
        self.myGPIOs = dict()
        json_parser.readconfig(self.myGPIOs, "inputs_def.xml")
        gpio_controler.setupInput(self.myGPIOs)
        
    def my_callback(self, channel):
        # appelé en cas de modif d'une entrée
        print('gpio callback :' + str(channel) + " : vaut : " + str(GPIO.input(channel)))
        gpio_controler.readgpios(self.myGPIOs)
        in_json = json_parser.write_json(self.myGPIOs, encode = True)
        self.sendMessage(in_json)
        print("message parti!")
        

    def onOpen(self):
        print("WebSocket connection open.")
        for key in self.myGPIOs.keys():
            GPIO.add_event_detect(self.myGPIOs[key].pin, GPIO.BOTH, callback = self.my_callback, bouncetime=100)
            # same callback for all pins. bouncetime in ms
            print("inputs : " + key + " : " + self.myGPIOs[key].value + " on pin : " + str(self.myGPIOs[key].pin))

    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
            print("Text message received: {0}".format(payload.decode('utf8')))

        # echo back message verbatim
        # self.sendMessage(payload, isBinary)

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))
        gpio_controler.close()
        


if __name__ == '__main__':
    import asyncio

    factory = WebSocketServerFactory(u"ws://127.0.0.1:9001")
    factory.protocol = MyServerProtocol

    loop = asyncio.get_event_loop()
    coro = loop.create_server(factory, '127.0.0.1', 9001)
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.close()
        loop.close()
