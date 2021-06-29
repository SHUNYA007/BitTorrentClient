# __init__.py
from bencoding import Decoder,Encoder
from hashlib import sha1
import random
from urllib.parse import urlencode
import requests
from torrentData import Torrent
from bencoding import Encoder
import socket
import struct
import logging


MAX_PEERS_TRY_CONNECT = 30
MAX_PEERS_CONNECTED = 8
logging.basicConfig(filename='logs.log',level=logging.DEBUG,format='%(levelname)s: %(message)s')

class SockAddr:
    def __init__(self, ip, port, allowed=True):
        self.ip = ip
        self.port = port
        self.allowed = allowed

    def __hash__(self):
        return "%s:%d" % (self.ip, self.port)
class Tracker_Request:
    """docstring for Tracker_Request."""

    def __init__(self,file):
        self.torrent=Torrent(file).get_torrent_data()
        self.connected_peers={}
        self.dict_sock_addr={}
    def connect_to_peers(self):
            for url in self.torrent.announce_list:
                url=url[0].decode()
                if url.startswith('http'):
                    try:
                        self.handle_http(url)
                    except:
                        logging.error('Failed to get peerslist from:',url)
                elif url.startswith('udp'):
                    try:
                        self.handle_udp(url)
                    except:
                        logging.error('Failed to get peerlist from:',url)
                else:
                    print("can't handle this",url)
    def handle_http(self,tracker):
        params = {
            'info_hash': self.torrent.info_hash,
            'peer_id': self.torrent.peer_id,
            'uploaded': 0,
            'downloaded': 0,
            'port': 6881,
            'left': self.torrent.total_length,
            'event': 'started'
        }
        try:
            answer_tracker = requests.get(tracker, params=params, timeout=5)
            self.list_peers=Decoder(answer_tracker.content).decode()
            offset=0
            if not b'failure reason' in self.list_peers:
                if not type(self.list_peers[b'peers']) == dict:
                    for _ in range(len(self.list_peers[b'peers'])//6):
                        ipaddr  =   struct.unpack_from("!i", self.list_peers[b'peers'], offset)[0]
                        ipaddr  =   socket.inet_ntoa(struct.pack("!i", ipaddr))
                        offset  +=  4
                        port   =   struct.unpack_from("!H", self.list_peers[b'peers'], offset)[0]
                        offset  +=  2
                        ipobj=SockAddr(ipaddr,port)
                        self.dict_sock_addr[ipobj.__hash__()]=ipobj

                else:
                    for p in self.list_peers['peers']:
                        s = SockAddr(p['ip'], p['port'])
                        self.dict_sock_addr[s.__hash__()] = s
        except Exception as e:
            logging.warning("HTTP scraping failed: %s" % e.__str__())

    def handle_udp(self,url):
        # print('handling udp',url)
        pass
