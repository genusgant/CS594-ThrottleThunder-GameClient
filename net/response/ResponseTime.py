from traceback import print_exc

from common.Constants import Constants
from net.response.ServerResponse import ServerResponse

class ResponseTime(ServerResponse):

    def execute(self, data):
        #print "Time Response"

        try:
            test = data.getInt32()
            if test == 1:
                #isDDGame is True when it is DD Game False otherwise
                if not self.worldMgr.isDDGame:
                    self.world.dashboard.force_timer(data.getInt32())
            elif test == 0:
                self.worldMgr.countdownTime = data.getInt32()
                self.worldMgr.startGameFlag = True

            # I think we are going to have 1 returned to the user, after the Server
            # Registers that they took damage.

        except:
            self.log('Bad [' + str(Constants.SMSG_TIME) + '] Time Response')
            print_exc()
