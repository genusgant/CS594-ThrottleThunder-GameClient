from Network.ServerConnection import ServerConnection
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from panda3d.core import NetDatagram

class GroupConnectionModel(ServerConnection):
    CODE_SEND_MSG = 116
    CODE_RESP_INV_MSG = 118
    CODE_RECV_INV_MSG = 216
    CODE_RECV_GRP_MSG = 218
    
    def __init__(self,menu):
        self.menu = menu
        self.parseInviteResponse = None
        self.parseUpdateResponse = None
        
    def getConnectionActions(self):
        return [[self.CODE_RESP_INV_MSG, self.getInviteMessage],
                [self.CODE_RECV_GRP_MSG, self.getUpdateMessage]];
    
    def sendInviteMessage(self,recipient):
        print "Sending invite to", recipient
        request = self.buildRequestPackage(self.CODE_SEND_MSG)
        request.addString(recipient)
        ServerConnection.sendMessage(self,request)
        
    def sendResponseMessage(self, message):
        request = self.buildRequestPackage(self.CODE_READY_MSG)
        request.addInt32(message)
        ServerConnection.sendMessage(self,request)
        
    def getInviteMessage(self,data):    
        fromName = data.getString()
        self.parseInviteResponse(fromName)    
        
    def getUpdateMessage(self,data):
        print "Group Update Message received"
        length = data.getInt32()
        players = []
        for i in range(length):
            players.append([data.getString(),data.getInt32()]) 
        self.parseUpdateResponse(players)
    
    def setHandler(self, invhandler, updhandler):
        self.parseInviteResponse = invhandler
        self.parseUpdateResponse = updhandler
    