from traceback import print_exc

from common.Constants import Constants
from net.response.ServerResponse import ServerResponse

class ResponseDisconnect(ServerResponse):

    def execute(self, data):

        try:
            username = data.getString()
            self.world.vehiclelist[username].chassisNP.remove()
            #self.world.vehiclelist[username].chassisNode.remove()
            self.world.vehiclelist.pop(username)

        except:
            self.log('Bad [' + str(Constants.SMSG_DISCONNECT) + '] Disconnect Response')
            print_exc()
