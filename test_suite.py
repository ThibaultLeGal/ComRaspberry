import unittest
from MonPaquet import json_parser
from MonPaquet import client_sys
from MonPaquet import client_banc
import asyncio


class MyTestCases(unittest.TestCase) :

    def printGpios(self):
        print("--GPIOs--")
        for key in self.myGpios.keys():
            print(key + " vaut : " + self.myGpios[key].value)
        print("--GPIOs--")

    def step(self):
        json_gpios = json_parser.write_json(self.myOutputs, True)
        client_sys.SysClientProtocol.sendExtJson(json_gpios)

    def setUp(self):
        print('--setup--')
        # check/establish connection
        # read conf
        # ect...

        OutputsIpAdress = '127.0.0.1'
        #OutputsIpAdress = '172.23.240.29'
        InputsIpAdress = '127.0.0.1'

        # create connection with sys
        self.factory_sys = client_sys.WebSocketClientFactory(u"ws://" + OutputsIpAdress + ":9000")
        self.factory_sys.protocol = client_sys.SysClientProtocol

        # create connection with banc
        self.factory_banc = client_banc.WebSocketClientFactory(u"ws://" + OutputsIpAdress + ":9001")
        self.factory_banc.protocol = client_banc.BancClientProtocol

        self.loop_sys = asyncio.get_event_loop()
        coro = self.loop_sys.create_connection(self.factory_sys, OutputsIpAdress, 9000)
        self.loop_banc = asyncio.get_event_loop()
        corob = self.loop_banc.create_connection(self.factory_banc, InputsIpAdress, 9001)

        self.loop_sys.run_until_complete(coro)
        self.loop_sys.run_forever()

        self.loop_banc.run_until_complete(corob)
        self.loop_banc.run_forever()

        #build gpio list
        self.myOutputs = dict()
        json_parser.readconfig(self.myOutputs, "gpio_def.xml")
        assert self.myOutputs.__len__() > 0
        self.myInputs = dict()
        json_parser.readconfig(self.myInputs, "inputs_def.xml")
        assert self.myInputs.__len__() > 0


    def runTest(self):
        print("--TestBody--ts")
        #corps du test

        self.step()

        self.myOutputs["LED1"].setValue("On")
        self.myOutputs["LED2"].setValue("Off")
        self.myOutputs["LED3"].setValue("Off")

        self.step()

        self.myOutputs["LED1"].setValue("Off")
        self.myOutputs["LED2"].setValue("On")
        self.myOutputs["LED3"].setValue("Off")

        self.step()

        self.myOutputs["LED1"].setValue("Off")
        self.myOutputs["LED2"].setValue("Off")
        self.myOutputs["LED3"].setValue("On")
        self.myOutputs["LED3"].setValue("On")

        self.step()

    def tearDown(self):
        print("--TearDown--")
        #close connections
        #client.sendClose()

        client_sys.SysClientProtocol.Quit()
        client_banc.BancClientProtocol.Quit()

        self.loop_sys.stop()
        self.loop_sys.close()

        self.loop_banc.stop()
        self.loop_banc.close()

def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(MyTestCases))
    return test_suite


"""
def load_tests(loader, tests, pattern):
    ''' Discover and load all unit tests in all files named ``*_test.py`` in ``./src/``
    '''
    suite = unittest.TestSuite()
    for all_test_suite in unittest.defaultTestLoader.discover('src', pattern='tests_*.py'):
        for test_suite in all_test_suite:
            suite.addTests(test_suite)
    return suite
"""

if __name__ == '__main__':
    ma_suite = suite()
    runner = unittest.TestSuite()
    runner.run(ma_suite)
