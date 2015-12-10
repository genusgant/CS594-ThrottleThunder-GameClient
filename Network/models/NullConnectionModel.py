from Network.ServerConnection import ServerConnection
from direct.distributed.PyDatagram import PyDatagram

class NullConnectionModel(ServerConnection):
    CODE_SEND_NULL=0
    
    def getConnectionActions(self):
        return [];
    
    def sendNull(self):
        request = self.buildRequestPackage(self.CODE_SEND_NULL)
        ServerConnection.sendMessage(self,request)