from Network.ServerConnection import ServerConnection
from direct.distributed.PyDatagram import PyDatagram

class AuthConnectionModel(ServerConnection):
    CODE_SEND_AUTH=101
    CODE_RESP_AUTH=201
    
    CODE_SEND_REG =103
    CODE_RESP_REG=203
    
    def __init__(self,screenModel):
        self.screenModel = screenModel
        
    def getConnectionActions(self):
        return [
                [self.CODE_RESP_AUTH, self.getAuth],
                
                [self.CODE_RESP_REG, self.getReg],
                ];
    
    def sendLoginRequest(self,username,password):
        request = self.buildRequestPackage(self.CODE_SEND_AUTH)
        request.addString(username)
        request.addString(password)
        ServerConnection.sendMessage(self,request)
        
    def sendRegisterRequest(self,username,password):
        request = self.buildRequestPackage(self.CODE_SEND_REG)
        request.addString(username)
        request.addString(password)
        request.addString("")
        ServerConnection.sendMessage(self,request)
    
    def getAuth(self, data):
        self.screenModel.parseAuthResponse(data.getUint16())

    def getReg(self, data):
        self.screenModel.parseRegResponse(data.getUint16())
        