from traceback import print_exc

from common.Constants import Constants
from net.response.ServerResponse import ServerResponse

class ResponseDisconnect(ServerResponse):

    def execute(self, data):

        try:
            username = data.getString()

            print "isDDGame Disconnect Response"

            if self.worldMgr.isDDGame:
                print "isDDGame"
                if username in self.world.vehiclelist.keys():
                    vehicle = self.world.vehiclelist[username]
                    vehicle.props.health = vehicle.props.armor = 0
                    vehicle.isDead = True
                    vehicle.remove(self.world)
                    # self.world.vehiclelist.pop(username)
                    self.world.deadCounter +=1
                    #del self.world.vehiclelist[self.username]
                    #self.world.vehiclelist[username].chassisNP.remove()
                    # self.world.vehiclelist[username].remove(self.world)
                    #self.world.world.removeVehicle(self.world.vehiclelist[username].vehicle)
                    #self.world.vehiclelist[username].chassisNode.remove()
                    # self.world.vehiclelist.pop(username)
                    print "deadCounter :",self.world.deadCounter
                    print "vehicle :",len(self.world.vehiclelist)
                    if self.world.deadCounter == len(self.world.vehiclelist)-1:
                        print "Last Man Standing"
                        self.world.gameEnd()
            # else:  # for RR game
                        
        except:
            self.log('Bad [' + str(Constants.SMSG_DISCONNECT) + '] Disconnect Response')
            print_exc()
