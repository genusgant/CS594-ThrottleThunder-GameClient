from traceback import print_exc

from common.Constants import Constants
from net.response.ServerResponse import ServerResponse

class ResponseReady(ServerResponse):

    def execute(self, data):

        try:
            self.username = data.getString()

            # for x in range(0, self.playerCount-1)
            #     self.readyPlayers[data.getString()] = data.getInt32()
            print "ResponseReady - ",self.username
            if self.username == self.world.mainCharRef.username:
                self.world.responseValue = 1


        except:
            self.log('Bad [' + str(Constants.SMSG_READY) + '] Ready Response')
            print_exc()
