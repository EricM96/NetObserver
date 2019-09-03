from autobahn.twisted.websocket import WebSocketServerProtocol
from os import getcwd
from tinydb import TinyDB, Query
from tinydb.operations import increment
import ujson, time, pprint 

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
        self._pp = pprint.PrettyPrinter(indent=2)

        self.this_is_a_test = 0

    def onConnect(self, request):
        print("Incoming connection from: {}".format(request.peer))

    def onOpen(self):
        print("Websocket connection now open")

    def onMessage(self, payload, isBinary):
        msg = ujson.loads(payload)
        self._process_msg(msg)
        self.this_is_a_test += 1
        print(self.this_is_a_test, "messages received")

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {}".format(reason))

    def _process_msg(self, msg):
        in_pkts, out_pkts, ip  = msg['in'], msg['out'], msg['ip']
        # print('Message received from: {}'.format(ip))
       
        if ip in self._current_window.keys():
            self._current_window[ip]['in'] += in_pkts
            self._current_window[ip]['out'] += out_pkts

        else:
            print('New entry made in window for ip address: {}'.format(ip))
            
            self._current_window[ip] = {'in': in_pkts, 'out': out_pkts}
            self._pp.pprint(self._current_window)

        if time.time() > self._time_to_update:
            self._reset_time()
            self._epochs_since_commit += 1 
            # print("Processing epoch {}".format(self._epochs_since_commit))
            self._current_frame[str(self._epochs_since_commit)] = self._current_window
            self._current_window = {} 

            if self._epochs_since_commit >= 4:
                self._epochs_since_commit = 0
                self._pp.pprint(self._current_frame)
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
            