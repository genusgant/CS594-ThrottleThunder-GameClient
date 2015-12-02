from traceback import print_exc

from common.Constants import Constants
from net.response.ServerResponse import ServerResponse

class ResponseSetRank(ServerResponse):

    def execute(self, data):

        try:
            self.rank = data.getInt32()

            # I think we are going to have 1 returned to the user, after the Server
            # Registers that they took damage.

        except:
            self.log('Bad [' + str(Constants.SMSG_SET_RANK) + '] Set Rank Response')
            print_exc()
