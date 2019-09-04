import sys, os 
sys.path.append(os.getcwd() + '/resources')

from autobahn.twisted.websocket import WebSocketServerProtocol
from twisted.enterprise import adbapi 
from os import getcwd
from tinydb.operations import increment
import ujson, time, pprint 
from dbms import DBMS

class ObserverWebSocketProtocol(WebSocketServerProtocol):
    def __init__(self):
        super().__init__()
        self._dbms = DBMS('/home/eam96/Development/NetObserver/observer/data/data.json')

    def onConnect(self, request):
        print("Incoming connection from: {}".format(request.peer))

    def onOpen(self):
        print("Websocket connection now open")

    def onMessage(self, payload, isBinary):
        msg = ujson.loads(payload)
        ip, in_pkts, out_pkts = msg['ip'], msg['in'], msg['out']
        self._dbms.process(ip, in_pkts, out_pkts)

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {}".format(reason))
            