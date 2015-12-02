from traceback import print_exc

from common.Constants import Constants
from net.response.ServerResponse import ServerResponse

class ResponseSetReady(ServerResponse):

    def execute(self, data):

        try:
            username = data.getString()

            # I think we are going to have 1 returned to the user, after the Server
            # Registers that they took damage.

        except:
            self.log('Bad [' + str(Constants.SMSG_SET_READY) + '] Set Ready Response')
            print_exc()
