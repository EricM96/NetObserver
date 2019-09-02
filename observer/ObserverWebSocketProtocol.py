class ObserverWebSocketProtocol(WebSocketServerProtocol):

    def onConnect(self, request):
        print("Incoming connection from: {}".format(request.peer))

    def onOpen(self):
        print("Websocket connection now open")

    def onMessage(self, payload, isBinary):
        print("Message received: {}".format(payload))

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {}".format(reason))
