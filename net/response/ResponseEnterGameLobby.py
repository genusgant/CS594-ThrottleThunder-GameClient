from traceback import print_exc

from common.Constants import Constants
from net.response.ServerResponse import ServerResponse
# from finalhw1 import Character
from Character import Character


class ResponseEnterGameLobby(ServerResponse):

    def execute(self, data):

        try:
            self.playerId = data.getString()
            self.validate = data.getUint16()

            if self.playerId != self.world.mainCharRef.playerId:
              char = Character(self.world, self.world.bulletWorld, 0,self.playerId)

              self.world.characters.append(char)
            else :
              self.world.responseValue = self.validate

            print "ResponseEnterGameLobby - ", self.playerId, " validate:", self.validate

            #self.log('Received [' + str(Constants.RAND_STRING) + '] String Response')

        except:
            self.log('Bad [' + str(Constants.SMSG_ENTER_GAME_LOBBY) + '] String Response')
            print_exc()
