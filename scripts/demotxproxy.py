
""" This demo will run two antenna simulators then run a proxy
which will connect to both
"""

import sys, os
from katcp.txbase import ProxyKatCP, DeviceHandler
from twisted.internet import reactor
from twisted.internet.protocol import ProcessProtocol
from twisted.python import log

class DemoProxy(ProxyKatCP):
    production = True
    
    def devices_scan_complete(self):
        print "Devices successfully scanned"
    
    def setup_devices(self):
        self.add_device(DeviceHandler('ant1', 'localhost', 1221))
        self.add_device(DeviceHandler('ant2', 'localhost', 1222))

PORT = 1236 # or 0

class KatLaunchProtocol(ProcessProtocol):
    def __init__(self, name):
        self.name = name
    
    def connectionMade(self):
        pass

    def outReceived(self, out):
        print out

    def errReceived(self, err):
        print err

    def processExited(self, status):
        if status.value.exitCode:
            print ("Running %s failed, check if kat-launch2.py is on your path,"
                   " exiting" % self.name)
            reactor.stop()
            return

def main():
    factory = DemoProxy(PORT, '')
    log.startLogging(open('demo.log', 'w'), setStdout=False)
    print "Listening on: " + str(factory.start().getHost())
    # we assume here that kat-launch2.py is executable and on PATH
    reactor.spawnProcess(KatLaunchProtocol('antenna1'), 'kat-launch2.py',
                         ['kat-launch2.py', 'antenna-sim', '--addr',
                          '127.0.0.1:1221', '--test-addr', '127.0.0.1:1222',
                          'ant1'],
                         env=os.environ)
    reactor.spawnProcess(KatLaunchProtocol('antenna2'), 'kat-launch2.py',
                         ['kat-launch2.py', 'antenna-sim', '--addr',
                          '127.0.0.1:1223', '--test-addr', '127.0.0.1:1224',
                          'ant2'],
                         env=os.environ)
    reactor.run()

if __name__ == '__main__':
    main()
