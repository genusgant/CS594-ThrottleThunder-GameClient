from traceback import print_exc

from common.Constants import Constants
from net.response.ServerResponse import ServerResponse

class ResponseChangeHealth(ServerResponse):

    def execute(self, data):

        try:
            username = data.getString()
            health = data.getInt32()

            # Need to set Heading and use keys
            if self.world.login != username and username in self.world.vehiclelist.keys():
                vehicle = self.world.vehiclelist[username]
                vehicle.setPropHealth(health)

            print "ResponseChangeHealth - ",username, " ", health

        except:
            self.log('Bad [' + str(Constants.RAND_STRING) + '] String Response')
            print_exc()
