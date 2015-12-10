from Network.ServerConnection import ServerConnection
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from panda3d.core import NetDatagram
from locale import currency

class GarageConnectionModel(ServerConnection):
    CODE_SEND_DETAILS = 120
    CODE_RECV_DETAILS = 220
    
    CODE_SEND_PURCHASE = 121
    CODE_RECV_PURCHASE = 221
    
    CODE_SEND_CURRENCY = 132
    CODE_RECV_CURRENCY = 232
    
    def __init__(self,callback):
        self.callback = callback
        self.parseDetailResponse = None
        self.parsePurchaseResponse = None
        self.parseCurrencyResponse = None
        
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
        armor = data.getInt()
        health = data.getInt()
        acceleration = data.getInt()
        speed = data.getInt()
        self.parseDetailResponse(armor, health, acceleration, speed)
        
    def sendPurchase(self,carId,typeId,value):
        request = self.buildRequestPackage(self.CODE_SEND_PURCHASE)
        request.addInt32(carId)
        request.addInt32(typeId)
        request.addInt32(value)
        ServerConnection.sendMessage(self,request)
        
    def getPurchaseMessage(self,data):
        status = data.getInt()
        self.parsePurchaseResponse(status)
            
    def sendCurrency(self):
        request = self.buildRequestPackage(self.CODE_SEND_PURCHASE)
        ServerConnection.sendMessage(self,request)
        
    def getCurrencyMessage(self,data):
        currency = data.getInt()
        self.parseCurrencyResponse(currency)
    
    def setHandler(self, detailHandler, purchaseHandler, currencyHandler):
        self.parseDetailResponse = detailHandler
        self.parsePurchaseResponse = purchaseHandler
        self.parseCurrencyResponse = currencyHandler