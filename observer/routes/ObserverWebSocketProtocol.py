from autobahn.twisted.websocket import WebSocketServerProtocol
from os import getcwd
from tinydb import TinyDB, Query
from tinydb.operations import increment
import ujson, time

class ObserverWebSocketProtocol(WebSocketServerProtocol):
    def __init__(self):
        super().__init__()
        self._db = TinyDB(getcwd() + '/data/data.json')
        self._dbq = Query()

        self._time_to_update = time.time() + 15
        self._epochs_since_commit = 0

        self._current_frame = {'1': None,
                               '2': None,
                               '3': None,
                               '4': None
                               } 
        self._current_window = {} 

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
       
        if ip in self._current_window.keys():
            self._current_window[ip][field] += 1 
        else:
            self._current_window[ip] = {'in': 0, 'out': 0}
            self._current_window[ip][field] += 1 

        if time.time() > self._time_to_update:
            self._epochs_since_commit += 1 
            self._current_frame[str(self._epochs_since_commit)] = self._current_window
            self._current_window = {} 

            if self._epochs_since_commit >= 4:
                self._db.insert(self._current_frame) 
                self._current_frame = {'1': None,
                                       '2': None,
                                       '3': None,
                                       '4': None
                }
                                        

    def _reset_time(self):
        self._time_to_update = time.time() + 15

    def _commit(self):
        self._db.insert(self._current_frame)
            