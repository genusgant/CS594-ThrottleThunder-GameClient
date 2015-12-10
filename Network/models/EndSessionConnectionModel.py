from Network.ServerConnection import ServerConnection
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from panda3d.core import NetDatagram

class EndSessionConnectionModel(ServerConnection):
    CODE_SEND_SAVE = 119
    CODE_RECV_SAVE = 219
    
    def __init__(self,callback):
        self.callback = callback
        
    def getConnectionActions(self):
        return [[self.CODE_RECV_SAVE, self.getMessage]];
    
    def sendMessage(self,pos,h):
        request = self.buildRequestPackage(self.CODE_SEND_SAVE)
        request.addString(str(pos[0])+","+str(pos[1])+","+str(pos[2])+","+str(h))
        ServerConnection.sendMessage(self,request)
        
    def getMessage(self,data):
        self.callback(data.getUint16())