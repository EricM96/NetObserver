import sys, os 
sys.path.append(os.getcwd() + '/resources')

from autobahn.twisted.websocket import WebSocketServerProtocol
from os import getcwd
from tinydb.operations import increment
import ujson, time, pprint 
from dbms import DBMS

class ObserverWebSocketProtocol(WebSocketServerProtocol):
    def __init__(self):
        super().__init__()
        self._dbms = DBMS('/home/eam96/Development/NetObserver/observer/data/data.json')
        # self._db = TinyDB(getcwd() + '/data/data.json')
        # self._dbq = Query()

        # self._time_to_update = time.time() + 15
        # self._epochs_since_commit = 0

        # self._current_frame = {'1': None,
        #                        '2': None,
        #                        '3': None,
        #                        '4': None
        #                        } 
        # self._current_window = {} 
        # self._pp = pprint.PrettyPrinter(indent=2)

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
            