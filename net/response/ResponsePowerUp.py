from traceback import print_exc

from common.Constants import Constants
from net.response.ServerResponse import ServerResponse

class ResponsePowerUp(ServerResponse):

    def execute(self, data):

        try:
            username = data.getString()
            powerId = data.getInt32()

            pickup = False
            if username == self.world.login:
                pickup = True
            self.world.powerups.resetPowerupsTask(powerId, pickup)

            if pickup:
                print "ResponsePowerPickUp for ME - ", powerId

        except:
            self.log('Bad [' + str(Constants.SMSG_POWER_UP) + '] Power Up Response')
            print_exc()
