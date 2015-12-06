from Network.ServerConnection import ServerConnection
from direct.distributed.PyDatagram import PyDatagram

class AuthConnectionModel(ServerConnection):
    CODE_SEND_AUTH=101
    CODE_RESP_AUTH=201
    
    CODE_SEND_DISCONNECT=102
    CODE_RESP_DISCONNECT=202
    
    CODE_SEND_REG =103
    CODE_RESP_REG=203
    
    def __init__(self,screenModel):
        self.screenModel = screenModel
        
    def getConnectionActions(self):
        return [
                [self.CODE_RESP_AUTH, self.getAuth],
                [self.CODE_RESP_DISCONNECT, self.getDisconnect],
                [self.CODE_RESP_REG, self.getReg],
                ];
    
    def sendLoginRequest(self,username,password):
        request = self.buildRequestPackage(self.CODE_SEND_AUTH)
        request.addString(username)
        request.addString(password)
        ServerConnection.sendMessage(self,request)
        
    def sendDisconnectRequest(self):
        request = self.buildRequestPackage(self.CODE_SEND_DISCONNECT)
        ServerConnection.sendMessage(self,request)
        
    def sendRegisterRequest(self,username,password):
        request = self.buildRequestPackage(self.CODE_SEND_REG)
        request.addString(username)
        request.addString(password)
        request.addString("")
        ServerConnection.sendMessage(self,request)
    
    def getAuth(self, data):
        self.screenModel.parseAuthResponse(data.getUint16())
        
    def getDisconnect(self, data):
        try:
            username = data.getString()
            if self.world.vehiclelist[username] != None :
                self.world.vehiclelist[username].chassisNP.remove()
                #self.world.vehiclelist[username].chassisNode.remove()
                self.world.vehiclelist.pop(username)

        except:
            print "Something went wrong"

    def getReg(self, data):
        self.screenModel.parseRegResponse(data.getUint16())
        