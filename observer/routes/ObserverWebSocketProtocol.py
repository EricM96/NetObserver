from autobahn.twisted.websocket import WebSocketServerProtocol
from tinydb import TinyDB
import time, pprint, ujson

db = TinyDB('/home/eam96/Development/NetObserver/observer/data/data.json')

time_to_update = time.time() + 15
epochs_since_commit = 0

current_frame = {'1': None, '2': None, '3': None, '4': None} 
current_window = {} 
pp = pprint.PrettyPrinter(indent=2)


class ObserverWebSocketProtocol(WebSocketServerProtocol):

    def onConnect(self, request):
        print("Incoming connection from: {}".format(request.peer))

    def onOpen(self):
        print("Websocket connection now open")

    def onMessage(self, payload, isBinary):
        msg = ujson.loads(payload)
        ip, in_pkts, out_pkts = msg['ip'], msg['in'], msg['out']
        global time_to_update, epochs_since_commit, current_frame,\
               current_window, pp, db

        if time.time() > time_to_update: 
            time_to_update = time.time() + 15
            epochs_since_commit += 1 
            print("Processing epoch {}".format(epochs_since_commit))
            current_frame[str(epochs_since_commit)] = current_window
            current_window = {} 

            if epochs_since_commit >= 4:
                epochs_since_commit = 0
                pp.pprint(current_frame)
                db.insert(current_frame) 
                current_frame = {'1': None, '2': None, '3': None, '4': None}
   
        if ip in current_window.keys():
            current_window[ip]['in'] += in_pkts
            current_window[ip]['out'] += out_pkts

        else:
            print('New entry made in window for ip address: {}'.format(ip))
            
            current_window[ip] = {'in': in_pkts, 'out': out_pkts}
            pp.pprint(current_window)    

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {}".format(reason))
            