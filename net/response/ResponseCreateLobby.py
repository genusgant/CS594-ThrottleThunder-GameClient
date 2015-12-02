from traceback import print_exc

from common.Constants import Constants
from net.response.ServerResponse import ServerResponse
# from finalhw1 import Character
from Character import Character


class ResponseCreateLobby(ServerResponse):

    def execute(self, data):

        try:
            self.gameName = data.getString()
            self.valid = data.getUint16()
            self.owner = data.getString()

            if self.valid == 1:
                self.world.responseValue = 1
            elif self.valid == 0:
                self.world.responseValue = 0

        except:
            self.log('Bad [' + str(Constants.SMSG_CREATE_LOBBY) + '] String Response')
            print_exc()
