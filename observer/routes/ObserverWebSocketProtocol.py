from autobahn.twisted.websocket import WebSocketServerProtocol
from os import getcwd
from tinydb import TinyDB, Query
from tinydb.operations import increment
import ujson

class ObserverWebSocketProtocol(WebSocketServerProtocol):
    def __init__(self):
        super().__init__()
        self._db = TinyDB(getcwd() + '/data/data.json')
        self._dbq = Query()

    def onConnect(self, request):
        print("Incoming connection from: {}".format(request.peer))

    def onOpen(self):
        print("Websocket connection now open")

    def onMessage(self, payload, isBinary):
        msg = ujson.loads(payload)
        self._process_msg(msg)

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {}".format(reason))

    def _process_msg(self, msg):
        field, ip  = msg['payload'], msg['ip']
        if self._db.contains(self._dbq.ip == ip):
            self._db.update(increment(field), self._dbq.ip == msg['ip'])
        elif field == 'in':
            self._db.insert({'ip': ip, 'in': 1, 'out': 0})
        else:
            self._db.insert({'ip': ip, 'in': 0, 'out': 1})
            