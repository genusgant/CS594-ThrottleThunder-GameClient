from Network.ServerConnection import ServerConnection
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from panda3d.core import NetDatagram

class GarageConnectionModel(ServerConnection):
    CODE_SEND_DETAILS = 120
    CODE_RECV_DETAILS = 220
    
    CODE_SEND_PURCHASE = 121
    CODE_RECV_PURCHASE = 221
    
    CODE_SEND_CURRENCY = 132
    CODE_RECV_CURRENCY = 232
    
    def __init__(self,callback):
        self.callback = callback
        
    def getConnectionActions(self):
        return [
                [self.CODE_RECV_DETAILS, self.getDetailMessage],
                [self.CODE_RECV_PURCHASE, self.getPurchaseMessage],
                [self.CODE_RECV_CURRENCY, self.getCurrencyMessage],
                ];
    
    def sendDetail(self,carId,typeId):
        request = self.buildRequestPackage(self.CODE_SEND_DETAILS)
        request.addInt32(carId)
        request.addInt32(typeId)
        ServerConnection.sendMessage(self,request)
        
    def getDetailMessage(self,data):
        try:
            armor = data.getInt()
            health = data.getInt()
            acceleration = data.getInt()
            speed = data.getInt()
            
            print "Car Upgrades!"

        except:
            print "Something went wrong"
        
    def sendPurchase(self,carId,typeId,value):
        request = self.buildRequestPackage(self.CODE_SEND_PURCHASE)
        request.addInt32(carId)
        request.addInt32(typeId)
        request.addInt32(value)
        ServerConnection.sendMessage(self,request)
        
    def getPurchaseMessage(self,data):
        try:
            status = data.getInt()
            
            if status == 1:
                print "Upgrade Purchases!"
            else:
                print "Not enough money!"
                
        except:
            print "Something went wrong"
            
    def sendCurrency(self):
        request = self.buildRequestPackage(self.CODE_SEND_PURCHASE)
        ServerConnection.sendMessage(self,request)
        
    def getCurrencyMessage(self,data):
        try:
            currency = data.getInt()
            
            print "User has:", currency
                
        except:
            print "Something went wrong"