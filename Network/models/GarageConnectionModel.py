from Network.ServerConnection import ServerConnection
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from panda3d.core import NetDatagram
from locale import currency

class GarageConnectionModel(ServerConnection):
    CODE_SEND_CAR = 105
    CODE_RECV_CAR = 205
    
    CODE_SEND_DETAILS = 120
    CODE_RECV_DETAILS = 220
    
    CODE_SEND_PURCHASE = 121
    CODE_RECV_PURCHASE = 221
    
    CODE_SEND_CURRENCY = 134
    CODE_RECV_CURRENCY = 234
    
    def __init__(self,callback):
        self.callback = callback
        self.parseDetailResponse = None
        self.parsePurchaseResponse = None
        self.parseCurrencyResponse = None
        
    def getConnectionActions(self):
        return [
                [self.CODE_RECV_CAR, self.getCarMessage],
                [self.CODE_RECV_DETAILS, self.getDetailMessage],
                [self.CODE_RECV_PURCHASE, self.getPurchaseMessage],
                [self.CODE_RECV_CURRENCY, self.getCurrencyMessage],
                ];
                
    def sendCar(self,carId,paintId,tiresId):
        request = self.buildRequestPackage(self.CODE_SEND_CAR)
        request.addInt32(carId)
        request.addInt32(paintId)
        request.addInt32(tiresId)
        ServerConnection.sendMessage(self,request)
        
    def getCarMessage(self,data):
        status = data.getInt32()
        self.parseCarResponse(status)
    
    def sendDetail(self,carId,typeId):
        request = self.buildRequestPackage(self.CODE_SEND_DETAILS)
        request.addInt32(carId)
        request.addInt32(typeId)
        ServerConnection.sendMessage(self,request)
        
    def getDetailMessage(self,data):
        armor = data.getInt32()
        health = data.getInt32()
        acceleration = data.getInt32()
        speed = data.getInt32()
        self.parseDetailResponse(armor, health, acceleration, speed)
        
    def sendPurchase(self,carId,typeId):
        request = self.buildRequestPackage(self.CODE_SEND_PURCHASE)
        request.addInt32(carId)
        request.addInt32(typeId)
        ServerConnection.sendMessage(self,request)
        
    def getPurchaseMessage(self,data):
        status = data.getInt32()
        self.parsePurchaseResponse(status)
            
    def sendCurrency(self):
        request = self.buildRequestPackage(self.CODE_SEND_CURRENCY)
        ServerConnection.sendMessage(self,request)
        
    def getCurrencyMessage(self,data):
        currency = data.getInt32()
        self.parseCurrencyResponse(currency)
    
    def setHandler(self, carHandler, detailHandler, purchaseHandler, currencyHandler):
        self.parseCarResponse = carHandler
        self.parseDetailResponse = detailHandler
        self.parsePurchaseResponse = purchaseHandler
        self.parseCurrencyResponse = currencyHandler