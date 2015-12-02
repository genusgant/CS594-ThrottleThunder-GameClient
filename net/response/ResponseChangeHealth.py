from traceback import print_exc

from common.Constants import Constants
from net.response.ServerResponse import ServerResponse

class ResponseChangeHealth(ServerResponse):

    def execute(self, data):

        try:
            username = data.getInt32()
            health = data.getInt32()

            # Need to set Heading and use keys
            vehicle = self.world.vehiclelist[username]
            vehicle.setHealth(health)

            print "ResponseChangeHealth - ",username, " ", health

        except:
            self.log('Bad [' + str(Constants.RAND_STRING) + '] String Response')
            print_exc()
