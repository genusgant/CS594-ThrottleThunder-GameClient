from traceback import print_exc

from common.Constants import Constants
from net.response.ServerResponse import ServerResponse
from Character import Character


class ResponseEnterGameName(ServerResponse):

    def execute(self, data):

        try:
            self.playerId = data.getString()
            self.validate = data.getUint16()

            print "ResponseEnterGameLobby - ", self.playerId, " validate:", self.validate

            self.world.responseValue = self.validate

        except:
            self.log('Bad [' + str(Constants.SMSG_ENTER_GAME_NAME) + '] String Response')
            print_exc()
