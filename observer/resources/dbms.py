from tinydb import TinyDB, Query
import time, pprint

class DBMS(object):
    def __init__(self, route):
        print("new instance of database created")

        self.db = TinyDB(route)
        self.query = Query()

        self._time_to_update = time.time() + 15
        self._epochs_since_commit = 0

        self._current_frame = {'1': None, '2': None, '3': None, '4': None} 
        self._current_window = {} 
        self._pp = pprint.PrettyPrinter(indent=2)

    def process(self, ip, in_pkts, out_pkts):
        if time.time() > self._time_to_update:
            self._reset_time()
            self._epochs_since_commit += 1 
            print("Processing epoch {}".format(self._epochs_since_commit))
            self._current_frame[str(self._epochs_since_commit)] = self._current_window
            self._current_window = {} 

            if self._epochs_since_commit >= 4:
                self._epochs_since_commit = 0
                self._pp.pprint(self._current_frame)
                self.db.insert(self._current_frame) 
                self._current_frame = {'1': None, '2': None, '3': None, '4': None}
   
        if ip in self._current_window.keys():
            self._current_window[ip]['in'] += in_pkts
            self._current_window[ip]['out'] += out_pkts

        else:
            print('New entry made in window for ip address: {}'.format(ip))
            
            self._current_window[ip] = {'in': in_pkts, 'out': out_pkts}
            self._pp.pprint(self._current_window)                                     

    def _reset_time(self):
        self._time_to_update = time.time() + 15