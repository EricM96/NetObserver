#!/usr/bin/python3

import pyshark, json, os, netifaces
from websocket import create_connection
import ujson, time 

def config():
    with open(os.getcwd() + '/storage/config.json', 'r') as fin:
        return json.loads(fin.read())

def main():
    conf = config()
    ip = netifaces.ifaddresses(conf['interface'])[netifaces.AF_INET][0]['addr']
    msg = {'ip': ip, 'in': 0, 'out': 0}

    ws = create_connection(conf['observer'])

    cap = pyshark.LiveCapture(interface=conf['interface'], bpf_filter=conf['filter'])

    time_to_send = time.time() + 5

    for pkt in cap:
        # print('Handling a packet')
        # tmp_msg = msg
        # tmp_msg['payload'] = 'in' if ip == str(pkt.ip.src) else 'out'
        if ip == str(pkt.ip.src):
            msg['out'] +=1  
        else:
            msg['in'] += 1
        if time.time() > time_to_send:
            ws.send(ujson.dumps(msg))
            time_to_send = time.time() + 5
            msg = {'ip': ip, 'in': 0, 'out': 0}

if __name__ == '__main__':
    main()