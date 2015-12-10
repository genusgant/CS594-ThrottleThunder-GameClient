from Network.ServerConnection import ServerConnection
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from panda3d.core import NetDatagram

class FriendConnectionModel(ServerConnection):
    CODE_SEND_UPDATE_MSG = 113
    CODE_SEND_REQUEST_MSG = 114
    CODE_SEND_LIST_MSG = 112
    CODE_RECV_LIST_MSG = 212
    CODE_RECV_MSG = 213
    
    def __init__(self,menu):
        self.menu = menu
        self.parseUpdateResponse = None
        
    def getConnectionActions(self):
        return [[self.CODE_RECV_MSG, self.getUpdateMessage],
                [self.CODE_RECV_LIST_MSG, self.getFriendListMessage]];
    
    def sendRequestMessage(self,username):
        request = self.buildRequestPackage(self.CODE_SEND_REQUEST_MSG)
        request.addString(username)
        ServerConnection.sendMessage(self,request)

    def sendUpdateMessage(self,username, status):
        #status is 0 if accepting a request, 1 if removing a friend or rejecting request
        request = self.buildRequestPackage(self.CODE_SEND_UPDATE_MSG)
        request.addString(username)
        request.addInt32(status)
        ServerConnection.sendMessage(self,request)
        
    def sendFriendListRequest(self):
        request = self.buildRequestPackage(self.CODE_SEND_LIST_MSG)
        ServerConnection.sendMessage(self,request)
        
    def getFriendListMessage(self,data):
        friendCount = data.getInt32()
        friends = []
        for x in range(friendCount):
            friends.append(data.getString())
        self.friendUpdateResponse(friends)
            
    def getUpdateMessage(self,data):
        fromName = data.getString()
        status = data.getInt32()
        self.parseUpdateResponse(fromName, status)
    
    def setHandlers(self, parsehandler, friendhandler):
        self.parseUpdateResponse = parsehandler
        self.friendUpdateResponse = friendhandler
    