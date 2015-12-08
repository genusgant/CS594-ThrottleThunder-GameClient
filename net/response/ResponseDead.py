from traceback import print_exc

from common.Constants import Constants
from net.response.ServerResponse import ServerResponse

class ResponseDead(ServerResponse):

    def execute(self, data):

        try:
            self.username = data.getString()

            if self.username in self.world.vehiclelist.keys():
                vehicle = self.world.vehiclelist[self.username]
                vehicle.props.health = vehicle.props.armor = 0
                #Handle removing character when dead
                vehicle.remove()
                del self.world.vehiclelist[self.username]
                self.world.deadCounter +=1

                print  "deadCounter/vehiclelist :",self.world.deadCounter,"/",len(self.world.vehiclelist)

                if self.world.deadCounter == len(self.world.vehiclelist)-1:
                    print "Last Man Standing"
                    self.world.gameEnd()

                #vehicle.chassisNP.removeNode()

            print "ResponseDead - ",self.username
            #self.log('Received [' + str(Constants.RAND_STRING) + '] String Response')

        except:
            self.log('Bad [' + str(Constants.SMSG_DEAD) + '] Dead Response')
            print_exc()
