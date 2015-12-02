from traceback import print_exc

from common.Constants import Constants
from net.response.ServerResponse import ServerResponse

class ResponsePrizes(ServerResponse):

    def execute(self, data):

        try:
            self.itemId = data.getInt32()


            # Gives the user an item based on what the server responses with
            # Popup to show what they unlocked?

            #self.log('Received [' + str(Constants.RAND_STRING) + '] String Response')

        except:
            self.log('Bad [' + str(Constants.SMSG_PRIZES) + '] Prizes Response')
            print_exc()
