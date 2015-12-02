from Network.ServerConnection import ServerConnection
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from panda3d.core import NetDatagram

class HeartbeatConnectionModel(ServerConnection):
    CODE_SEND_MSG = 301
    CODE_RECV_MSG = 302
        
    def getConnectionActions(self):
        return [[self.CODE_RECV_MSG, self.getHeartbeat]];
    
    def sendHeartbeat(self):
        request = self.buildRequestPackage(self.CODE_SEND_MSG)
        ServerConnection.sendMessage(self,request)
        
    def getHeartbeat(self,data):
        self.doNothing = True