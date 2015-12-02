from traceback import print_exc

from common.Constants import Constants
from net.response.ServerResponse import ServerResponse

class ResponseDead(ServerResponse):

    def execute(self, data):

        try:
            username = data.getString()

            vehicle = self.world.vehiclelist[username]
            vehicle.remove()

            print "ResponseDead - ",self.username
            #self.log('Received [' + str(Constants.RAND_STRING) + '] String Response')

        except:
            self.log('Bad [' + str(Constants.SMSG_DEAD) + '] Dead Response')
            print_exc()
