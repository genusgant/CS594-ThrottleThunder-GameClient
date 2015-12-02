from traceback import print_exc

from common.Constants import Constants
from net.response.ServerResponse import ServerResponse

class ResponseTime(ServerResponse):

    def execute(self, data):
        print "Time Response"

        try:
            test = data.getInt32()
            if test == 1:
                self.world.dashboard.force_timer(data.getInt32())
            

            # I think we are going to have 1 returned to the user, after the Server
            # Registers that they took damage.

        except:
            self.log('Bad [' + str(Constants.SMSG_TIME) + '] Time Response')
            print_exc()
