from Network.ServerConnection import ServerConnection
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from panda3d.core import NetDatagram

class TimeConnectionModel(ServerConnection):
    #CODE_SEND_MSG = 0
    CODE_RECV_MSG = 229
    
    def __init__(self,menu):
        self.menu = menu
        self.parseTimeResponse = None
        
    def getConnectionActions(self):
        return [[self.CODE_RECV_MSG, self.getTime]];
            
    def getTime(self,data):
        seconds = data.getInt32()
        milliseconds = data.getLong64()
        
		if seconds == 0:
			self.parseTimeResponse(seconds, milliseconds)			
        
    def setHandlers(self, parsehandler):
        self.parseTimeResponse = parsehandler     
