from traceback import print_exc

from common.Constants import Constants
from net.response.ServerResponse import ServerResponse

class ResponsePowerUp(ServerResponse):

    def execute(self, data):

        try:
            username = data.getString()
            powerId = data.getInt32()


            vehicle = self.world.vehiclelist[username]

            #self.log('Received [' + str(Constants.RAND_STRING) + '] String Response')

            print "ResponsePowerUp - ", username, " ", powerId

        except:
            self.log('Bad [' + str(Constants.SMSG_POWER_UP) + '] Power Up Response')
            print_exc()
