from sys import stdout
from autobahn.twisted.websocket import WebSocketServerFactory
from twisted.python import log 
from twisted.internet import reactor
from routes.ObserverWebSocketProtocol import ObserverWebSocketProtocol

def main():
    log.startLogging(stdout)
    factory = WebSocketServerFactory('ws://127.0.0.1:8080')
    factory.protocol = ObserverWebSocketProtocol

    reactor.listenTCP(8080, factory)
    reactor.run() 

if __name__ == '__main__':
    main()