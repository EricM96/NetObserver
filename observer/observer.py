from autobahn.twisted.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory
from twisted.python import log 
from twisted.internet import reactor
from ObserverWebSocketProtocol import ObserverWebSocketProtocol
import sys

def main():
    log.startLogging(sys.stdout)
    factory = WebSocketServerFactory(u"ws://127.0.0.1:8080")
    factory.protocol = ObserverWebSocketProtocol

    reactor.listenTCP(8080, factory)
    reactor.run() 

if __name__ == '__main__':
    main()