from Network.BaseConnection                     import BaseConnection
from direct.distributed.PyDatagram              import PyDatagram
from direct.distributed.PyDatagramIterator      import PyDatagramIterator
from panda3d.core                               import NetDatagram

class ServerConnection(BaseConnection):
    MODEL_AUTH = 0
    
    CODE_INT = 1
    CODE_STRING = 2
    CODE_SHORT = 3
    CODE_FLOAT = 4
    
    def __init__(self):
        BaseConnection.__init__(self)
        self.recvActions = []
        
    def connect(self, host, port):
        if(self.cManager == None):
            self.host = host
            self.port = port
            BaseConnection.connect(self, host, port)
            taskMgr.add(self.updateRoutine,"NetworkMessages")
    
    def setupConnectionModel(self,model):
        model.cWriter = self.cWriter
        model.cListener = self.cListener
        model.cReader = self.cReader
        model.cManager = self.cManager
        model.connection = self.connection
        for Item in model.getConnectionActions():
            self.registerResponseAction(Item[0], Item[1])
        return model
    
    def registerResponseAction(self,code,func):
        self.recvActions.append([code,func])
    
    def intRequest(self, msg):
        pkg = PyDatagram()
        pkg.addUint16(1)
        pkg.addInt32(msg)
        return pkg
    
    def stringRequest(self, msg):
        pkg = PyDatagram()
        pkg.addUint16(101)
        pkg.addString(msg)
        return pkg
    
    def shortRequest(self, msg):
        pkg = PyDatagram()
        pkg.addUint16(3)
        pkg.addUint16(msg)
        return pkg
    
    def floatRequest(self, msg):
        pkg = PyDatagram()
        pkg.addUint16(4)
        pkg.addFloat32(msg)
        return pkg
        
    def buildRequestPackage(self,code):
        pkg = PyDatagram()
        pkg.addUint16(code)
        return pkg
    
    def sendMessage(self, request):
        self.cWriter.send(request,self.connection)
        #taskMgr.remove('message')
            
    def check(self):
        while self.cReader.dataAvailable():
            datagram = NetDatagram()
            # Retrieve the contents of the datagram.
            if self.cReader.getData(datagram):
                data = PyDatagramIterator(datagram)
                responseCode = data.getUint16()
                if responseCode == self.CODE_INT:
                    self.getInt(data)
                elif responseCode == self.CODE_STRING:
                    self.getString(data)
                elif responseCode == self.CODE_SHORT:
                    self.getShort(data)
                elif responseCode == self.CODE_FLOAT:
                    self.getFloat(data)
                else:
                    for recvAction in self.recvActions:
                        if(responseCode == recvAction[0]):
                            recvAction[1](data)
    
    def getInt(self, data):
        msg = data.getInt32()
        print "recieved ", msg
        
    def getString(self, data):
        msg = data.getString()
        print "recieved ", msg
    
    def getShort(self, data):
        msg = data.getUint16()
        print "recieved ", msg
    
    def getFloat(self, data):
        msg = data.getFloat32()
        print "recieved ", msg
    
    def updateRoutine(self,task):
        self.check()
        return task.again; 