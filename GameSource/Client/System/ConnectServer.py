import socket
import pickle
from Function import HandleFile

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.getHost()
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getHost(self):
        host = HandleFile.readFile("Host.json")
        self.server = host["host"]
        self.port = host["port"]

    def getPos(self):
        return self.p
    
    def connect(self):
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(32768))
        except:
            pass
        
    def send(self, data):
        try:
            self.client.sendall(pickle.dumps(data))
            return pickle.loads(self.client.recv(32768))
        except socket.error as e:
            print("err: ", e)
