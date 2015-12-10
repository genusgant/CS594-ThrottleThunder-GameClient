from traceback import print_exc

from common.Constants import Constants
from net.response.ServerResponse import ServerResponse

class ResponseSetPosition(ServerResponse):

    def execute(self, data):

        try:
            print "response set position"

            playerCount = data.getInt32()

            for x in range(0, playerCount):
                username = data.getString()
                #if username != self.world.login:
                    #carId = data.getInt32()
                    #carPaint = data.getInt32()
                    #carTires = data.getInt32()
                x= data.getFloat32()
                y= data.getFloat32()
                z= data.getFloat32()
                h= data.getFloat32()
                p= data.getFloat32()
                r= data.getFloat32()
                print "Set Position Updated for: ", username, "at- ", x,y,z,h,p,r
                self.worldMgr.modifyPlayerPos(username, x,y,z,h,p,r)
                    #self.world.createOtherVehicles(username, carId, carPaint, carTires, x,y,z,h,p,r)
                #else:
                    #self.world.vehicleContainer.chassisNP.setPosHpr(data.getFloat32(), data.getFloat32(), data.getFloat32(), data.getFloat32(),data.getFloat32(),data.getFloat32())

            self.worldMgr.otherPlayersDataAvailable = True
            #self.worldMgr.startGameSequence()
            print "otherPlayersDataAvailable & ResponseSetPosition Player Count - ", playerCount

            self.world.responseValue = 1

        except:
            self.log('Bad [' + str(Constants.SMSG_SET_POSITION) + '] Set Position Response')
            print_exc()
