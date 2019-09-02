#!/usr/bin/python3

import pyshark, json, os, netifaces
from websocket import create_connection
import ujson

def config():
    with open(os.getcwd() + '/storage/config.json', 'r') as fin:
        return json.loads(fin.read())

def main():
    conf = config()
    ip = netifaces.ifaddresses(conf['interface'])[netifaces.AF_INET][0]['addr']
    msg = {'ip': ip, 'payload' : ''}

    ws = create_connection(conf['observer'])


    cap = pyshark.LiveCapture(interface=conf['interface'], bpf_filter=conf['filter'])

    for pkt in cap:
        tmp_msg = msg
        tmp_msg['payload'] = 'in' if ip == str(pkt.ip.src) else 'out'
        ws.send(ujson.dumps(tmp_msg))

if __name__ == '__main__':
    main()