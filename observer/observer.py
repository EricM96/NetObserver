from autobahn.twisted.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory
from twisted.python import log 
from twisted.internet import reactor
import sys

class ObserverWebSocketProtocol(WebSocketServerProtocol):

    def onConnect(self, request):
        print("Incoming connection from: {}".format(request.peer))

    def onOpen(self):
        print("Websocket connection now open")

    def onMessage(self, payload, isBinary):
        print("Message received: {}".format(payload))

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {}".format(reason))

def main():
    log.startLogging(sys.stdout)
    factory = WebSocketServerFactory(u"ws://127.0.0.1:8080")
    factory.protocol = ObserverWebSocketProtocol

    reactor.listenTCP(8080, factory)
    reactor.run() 

if __name__ == '__main__':
    main()