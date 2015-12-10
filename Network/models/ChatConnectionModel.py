from Network.ServerConnection import ServerConnection
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from panda3d.core import NetDatagram



class ChatConnectionModel(ServerConnection):
    CODE_SEND_MSG = 106
    CODE_RECV_MSG = 206
    
    def __init__(self,screenModel):
        self.screenModel = screenModel
        self.parseResponse = self.__doNothing
        
    def getConnectionActions(self):
        return [[self.CODE_RECV_MSG, self.getChatMessage]];
    
    def sendChatMessage(self,message):
        request = self.buildRequestPackage(self.CODE_SEND_MSG)
        request.addString(message)
        ServerConnection.sendMessage(self,request)
        
    def getChatMessage(self,data):
        self.parseResponse(data.getString(),data.getString())
        
    def setHandler(self, handler):
        self.parseResponse = handler
    
    def __doNothing(one, two):
        pass
    