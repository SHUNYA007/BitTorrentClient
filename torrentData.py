"""Get torrent data from .torrent file
Store the data in a class"""
from hashlib import sha1
from bencoding import Decoder,Encoder
import os
import random
import time
import math

class Torrent(object):
    """class to properly structutre torrent data"""

    def __init__(self,file_name):
        self.file_name=file_name
        self.torrent_file = {}
        self.total_length: int = 0
        self.piece_length: int = 0
        self.pieces: int = 0
        self.info_hash: str = ''
        self.peer_id: str = ''
        self.announce_list = ''
        self.file_names = []
        self.number_of_pieces: int = 0


    def get_torrent_data(self):
        with open(self.file_name,'rb') as file:
            contents=file.read()
            self.torrent_file=Decoder(contents).decode()
        self.piece_length = self.torrent_file[b'info'][b'piece length']
        self.pieces = self.torrent_file[b'info'][b'pieces']
        self.info_hash=sha1(Encoder(self.torrent_file[b'info']).encode()).digest()
        self.peer_id=self.genrate_peer_id()
        self.announce_list=self.fetch_urls()
        self.handleFiles()
        self.number_of_pieces = math.ceil(self.total_length / self.piece_length)
        return self

    def handleFiles(self):
        info=self.torrent_file[b'info']
        folderName=info[b'name']
        if b'files' in info:
            if not os.path.exists(folderName):
                os.path.join(folderName)
            for file in info[b'files']:
                self.file_names.append({'name':file[b'path'][0].decode(),'length':file[b'length']})
                self.total_length+=file[b'length']

        else:
            self.file_names.append({"path": folderName , "length": info[b'length']})
            self.total_length = info[b'length']
    def fetch_urls(self):
        if b'announce-list' in self.torrent_file:
            return self.torrent_file[b'announce-list']
        return [[self.torrent_file['announce']]]
    def genrate_peer_id(self):
        seed = str(time.time())
        return sha1(seed.encode('utf-8')).digest()
