from Network.ServerConnection import ServerConnection
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from panda3d.core import NetDatagram

class QueueConnectionModel(ServerConnection):
    CODE_SEND_MSG = 111
    CODE_READY_MSG = 117
    CODE_RECV_MSG = 211
    
    def __init__(self,menu):
        self.menu = menu
        self.parseQueueResponse = None
        
    def getConnectionActions(self):
        return [[self.CODE_RECV_MSG, self.getQueueMessage]];
    
    def sendQueueMessage(self,message):
        request = self.buildRequestPackage(self.CODE_SEND_MSG)
        request.addInt32(message)
        ServerConnection.sendMessage(self,request)
        
    def sendReadyMessage(self, message):
        request = self.buildRequestPackage(self.CODE_READY_MSG)
        request.addInt32(message)
        ServerConnection.sendMessage(self,request)
        
    def getQueueMessage(self,data):
        print "getQueueMessage called"
        size = data.getInt32()
        sizeNeeded = data.getInt32()
        length = data.getInt32()
        players = []
        for i in range(length):
            players.append([data.getString(),data.getInt32()]) 
        self.parseQueueResponse(size, sizeNeeded, players)
    
    def setHandler(self, handler):
        self.parseQueueResponse = handler
    