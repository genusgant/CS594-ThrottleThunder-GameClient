#from direct.showbase.ShowBase import ShowBase
from panda3d.core import ConnectionWriter
from panda3d.core import QueuedConnectionListener
from panda3d.core import QueuedConnectionManager
from panda3d.core import QueuedConnectionReader

class BaseConnection:    
    def __init__(self):
        self.cManager = None
        self.cWriter = None
        self.cReader = None
        self.cListener = None
        self.connection = None
        
    def connect(self,host,port):
        self.cManager = QueuedConnectionManager()
        self.cListener = QueuedConnectionListener(self.cManager, 0)
        self.cReader = QueuedConnectionReader(self.cManager, 0)
        self.cWriter = ConnectionWriter(self.cManager, 0)
        
        self.connection = self.cManager.openTCPClientConnection(host, port, 10000)
        if self.connection:
            self.cReader.addConnection(self.connection)
            
    def close(self):
        if self.connection != None:
            self.cManager.closeConnection(self.connection)
            self.connection = None