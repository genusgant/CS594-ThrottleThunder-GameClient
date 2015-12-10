from traceback import print_exc

from common.Constants import Constants
from net.response.ServerResponse import ServerResponse

class ResponsePowerPickUp(ServerResponse):

    def execute(self, data):

        try:
            username = data.getString()
            powerId = data.getInt32()

        except:
            self.log('Bad [' + str(Constants.SMSG_POWER_UP_PICK_UP) + '] Power Pick Up Response')
            print_exc()
