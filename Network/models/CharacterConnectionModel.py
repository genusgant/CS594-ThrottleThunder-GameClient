from Network.ServerConnection import ServerConnection
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from panda3d.core import NetDatagram

class CharacterConnectionModel(ServerConnection):
    CODE_SEND_MSG = 106
    CODE_RECV_MSG = 206
    
    CODE_RECV_NP = 207
    CODE_RECV_DSC = 208
    
    def __init__(self,screenModel):
        self.screenModel = screenModel
        self.taskName = "updatePos"
        
    def getConnectionActions(self):
        return [
                [self.CODE_RECV_MSG,self.getLastPosition],
                [self.CODE_RECV_NP, self.getNewPlayer],
                [self.CODE_RECV_DSC, self.disconnectPlayer]
            ];
    
    def sendCharacter(self,message):
        request = self.buildRequestPackage(self.CODE_SEND_MSG)
        request.addString(message)
        ServerConnection.sendMessage(self,request)
        
    def getLastPosition(self,data):
        self.screenModel.parseResponse(data.getString())
        
    def getNewPlayer(self,data):
        self.screenModel.World.taskMgr.remove(self.taskName)
        username = data.getString()
        modelName = data.getString()
        self.screenModel.World.CharacterManager.createCharacter(username=username,modelName=modelName)
        self.screenModel.World.taskMgr.doMethodLater(0.2,self.updateCharacterPos,self.taskName)
        
    def disconnectPlayer(self,data):
        self.screenModel.World.CharacterManager.removeCharacter(data.getString())
        
    def updateCharacterPos(self,task):
        self.screenModel.World.MoveManager.sendUpdatePosition()