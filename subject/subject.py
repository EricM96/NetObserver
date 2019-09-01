#!/usr/bin/python3

import pyshark, json, os, netifaces
from websocket import create_connection

def config():
    with open(os.getcwd() + '/storage/config.json', 'r') as fin:
        return json.loads(fin.read())

def main():
    conf = config()
    ip = netifaces.ifaddresses(conf['interface'])[netifaces.AF_INET][0]['addr']

    ws = create_connection(conf['observer'])

    cap = pyshark.LiveCapture(interface=conf['interface'], bpf_filter=conf['filter'])
    for pkt in cap:
        ws.send(b'in') if ip == str(pkt.ip.src) else ws.send(b'out')

if __name__ == '__main__':
    main()